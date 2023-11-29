from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404

from app_api_connector.dataforseo import gg_api as DF_GG_API
from .forms import KeywordResearchForm
from .functions import serp_config_manage
from . import models

import time

class KeywordResearchView(LoginRequiredMixin, View):
	def get(self, request):
		context = {
			'country_data': DF_GG_API.COUNTRY_LIST,
			'language_data': DF_GG_API.get_language('2704', all_option=True),
		}
		template = 'app_market_explorer/keyword_research.html'
		return render(request, template_name=template, context=context)
	def post(self, request):
		form = KeywordResearchForm(request.POST)
		if not form.is_valid():
			messages.error(request, message=form.errors, extra_tags='ERROR')
			return redirect(reverse('keyword_research'))
		
		keyword = form.cleaned_data['keyword']
		language_code = form.cleaned_data['language_code']
		country_code = form.cleaned_data['country_code']

		filter_include = form.cleaned_data['filter_include']
		filter_exclude = form.cleaned_data['filter_exclude']
		filter_volume_min = form.cleaned_data['filter_volume_min']
		filter_volume_max = form.cleaned_data['filter_volume_max']

		serp_config = serp_config_manage.keyword_analytics_config(country_code, language_code)

		new_order = models.KeywordResearchOrderModel.objects.create(
			keyword = keyword,
			config = serp_config,
			filter_include = filter_include,
			filter_exclude = filter_exclude,
			filter_volume_min = filter_volume_min,
			filter_volume_max = filter_volume_max,
			creator = request.user
		)
		return redirect(reverse('keyword_research_result', args=[new_order.id] ))

@login_required
def keyword_research_result_view(request, id):
	try:
		obj = models.KeywordResearchOrderModel.objects.get(id=id)
	except:
		raise Http404()
	if obj.creator != request.user:
		raise PermissionDenied
	context = {
		'obj':obj,
		'country_data': DF_GG_API.COUNTRY_LIST,
		'language_data': DF_GG_API.get_language('2704', all_option=True),
	}
	template = 'app_market_explorer/keyword_research_result.html'
	return render(request, template_name=template, context=context)