from django.contrib import admin
from . import models
# Register your models here.

class SerpConfigAdmin(admin.ModelAdmin):
	list_display = ['country_code','location_code', 'language_code', 'device', 'se_domain']
	search_fields = ['country_code','location_code', 'language_code', 'device', 'se_domain']

class KeywordAnalysisAdmin(admin.ModelAdmin):
	list_display = ['name', 'project', 'serp_config', 'creator', 'create_time']
	list_filter = ['creator']
	search_fields = ['name']
	date_hierarchy = 'create_time'

class KeywordRootAdmin(admin.ModelAdmin):
	list_display = ['keyword', 'create_time']
	search_fields = ['keyword']
	date_hierarchy = 'create_time'

class VolumeOrderAdmin(admin.ModelAdmin):
	list_display = ['from_action', 'id_main',  'order_count', 'get_from_date', 'creator', 'create_time']
	search_fields = ['from_action', 'id_main']
	list_filter = ['from_action', 'id_main', 'get_from_date', 'creator']
	date_hierarchy = 'create_time'

admin.site.register(models.SerpConfigModel, SerpConfigAdmin)
admin.site.register(models.KeywordAnalysisModel, KeywordAnalysisAdmin)
admin.site.register(models.KeywordRootModel, KeywordRootAdmin)
admin.site.register(models.VolumeOrderModel, VolumeOrderAdmin)