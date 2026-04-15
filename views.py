# jobs/views.py
from django.shortcuts import render
from .models import Job
from django.db.models import Q
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse
from django.core.management import call_command

def run_scraper_view(request):
    secret_key = request.GET.get('secret_key', None)
    if secret_key != 'run-scraper-now-12345':
        return HttpResponse("Unauthorized", status=403)

    try:
        print("🚀 Starting scraper from the web...")
        
        # ===== THE FINAL, CORRECT SYNTAX =====
        # Positional arguments first, then named optional arguments.
        # This will now work because the cache is cleared.
        call_command('scrape_naukri', 'it', pages=5)
        
        print("🎉 Scraper run completed successfully!")
        return HttpResponse("Scraper run completed successfully!")

    except Exception as e:
        print(f"🔴 An error occurred during scraping: {e}")
        return HttpResponse(f"An error occurred: {e}", status=500)
    
    
def job_list(request):
    query = request.GET.get('q')
    jobs_list = Job.objects.all().order_by('-date_posted')

    if query:
        jobs_list = jobs_list.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )
    
    paginator = Paginator(jobs_list, 15) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj, 
        'query': query,
    }
    return render(request, 'jobs/job_list.html', context)



# ✅ New API Endpoint for scraper
@csrf_exempt
def ingest_jobs(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    token = request.headers.get('X-SCRAPER-TOKEN')
    if token != getattr(settings, 'SCRAPER_SECRET', None):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    jobs = data.get('jobs', [])
    saved = 0

    for job in jobs:
        ext_id = job.get('id') or job.get('job_url')
        title = job.get('title')
        company = job.get('company')
        location = job.get('location')
        salary = job.get('salary')
        description = job.get('description')
        job_url = job.get('job_url')

        if not job_url:
            continue

        obj, created = Job.objects.update_or_create(
            external_id=ext_id,
            defaults={
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'job_url': job_url,
            }
        )
        if created:
            saved += 1

    return JsonResponse({'status': 'ok', 'saved': saved})
