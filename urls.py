# jobs/urls.py
from django.urls import path
from .views import job_list, ingest_jobs
from .views import run_scraper_view

urlpatterns = [
    path('', job_list, name='job_list'),
    path('ingest_jobs/', ingest_jobs, name='ingest_jobs'),  # ✅ new API endpoint
    path('run-scraper/', run_scraper_view, name='run-scraper'),
]
