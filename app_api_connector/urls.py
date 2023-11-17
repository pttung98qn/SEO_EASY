from django.urls import path
from . import views, views_df

urlpatterns = [
    path('df/languages/<str:search_engine>/<int:country_code>', views_df.get_language, name='language_available'),
]