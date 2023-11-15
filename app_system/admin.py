from django.contrib import admin
from . import models
# Register your models here.
class ErrorLogAdmin(admin.ModelAdmin):
	list_per_page = 5000
	list_filter = ['error_name']
	date_hierarchy = 'error_timestamp'
	list_display = ['error_name','error_timestamp']

admin.site.register(models.ErrorLogModel, ErrorLogAdmin)