from django.apps import AppConfig


class AppCustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_customer'

    def ready(self):
        from . import signals