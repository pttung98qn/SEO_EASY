from django.urls import path
from . import views, views_serp

urlpatterns = [
    path('serp/', views_serp.DashboardView.as_view(), name='serp_dashboard'),

    path('serp/project/<int:id>/', views_serp.ProjectView.as_view(), name='serp_project'),
]