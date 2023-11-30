from django.contrib import admin
from . import models
# Register your models here.
class KeywordResearchRequestAdmin(admin.ModelAdmin):
	list_display = ['order','offset','copy','cost','status','turnarround_time']
	list_filter = ['copy', 'status', 'creator']
	date_hierarchy = 'create_time'

admin.site.register(models.KeywordResearchRequest, KeywordResearchRequestAdmin)