from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
	login_url='/customer/login/'
	def get(self, request):
		serp_dashboard_template = 'app_project_manage/serp_dashboard.html'
		return render(request, template_name=serp_dashboard_template)

class ProjectView(LoginRequiredMixin, View):
	login_url='/customer/login/'
	def get(self, request, id):
		context = {
			'avr_data':{},
			'pos_data':range(4),
			'top_compatitors': range(7),
		}
		serp_dashboard_template = 'app_project_manage/serp_project.html'
		return render(request, template_name=serp_dashboard_template, context=context)