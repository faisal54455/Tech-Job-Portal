from django.contrib import admin
from .models import Job
from import_export.admin import ImportExportModelAdmin 

class JobAdmin(ImportExportModelAdmin):
    list_display = ('title', 'company', 'location', 'date_posted')
    list_filter = ('company', 'location')
    search_fields = ('title', 'company', 'description')

    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'company', 'location', 'salary')
        }),
        ('Full Description', {
            'classes': ('collapse',), 
            'fields': ('description',),
        }),
        ('Meta Data', {
            'fields': ('job_url', 'date_posted')
        }),
    )
    readonly_fields = ('date_posted',) 


admin.site.register(Job, JobAdmin)