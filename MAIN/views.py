from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class DashboardView(LoginRequiredMixin , View):
    def get(self, request):
        template = 'dashboard.html'
        return render(request, template_name=template)


class DashboardSampleView(LoginRequiredMixin,TemplateView):
    pass
dashboard_view = DashboardSampleView.as_view(template_name = "dashboard_sample/index.html")
dashboard_analytics_view = DashboardSampleView.as_view(template_name = "dashboard_sample/dashboard-analytics.html")
dashboard_crypto_view = DashboardSampleView.as_view(template_name = "dashboard_sample/dashboard-crypto.html")
class MyPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    success_url = reverse_lazy("dashboard")
class MyPasswordSetView(LoginRequiredMixin,PasswordSetView):
    success_url = reverse_lazy("dashboard")

