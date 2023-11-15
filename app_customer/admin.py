from django.contrib import admin
from . import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'credit', 'online', 'beta_checker', 'last_visited', 'create_time']
    search_fields = ['user']
    list_filter = ['online', 'beta_checker']
    date_hierarchy = 'create_time'

class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['user','ip','device','user_agents','location','create_time']
    list_filter = ['user','ip','device', 'location']
    date_hierarchy = 'create_time'

admin.site.register(models.LoginLogModel, LoginLogAdmin)
admin.site.register(models.CustomerModel, CustomerAdmin)