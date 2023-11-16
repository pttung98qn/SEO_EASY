from django.contrib import admin
from . import models
# Register your models here.

class SerpConfigAdmin(admin.ModelAdmin):
	list_display = ['country_code','location_code', 'language_code', 'device', 'se_domain']
	# list_filter = ['country_code','location_code', 'language_code', 'device', 'se_domain']
	search_fields = ['country_code','location_code', 'language_code', 'device', 'se_domain']

class KeywordAnalysisAdmin(admin.ModelAdmin):
	list_display = ['name', 'project', 'serp_config', 'creator']
	list_filter = ['creator']
	search_fields = ['name']
	date_hierarchy = 'create_time'

admin.site.register(models.SerpConfigModel, SerpConfigAdmin)
admin.site.register(models.KeywordAnalysisModel, KeywordAnalysisAdmin)