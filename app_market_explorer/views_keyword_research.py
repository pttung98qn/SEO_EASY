from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from app_api_connector.dataforseo import gg_api as DF_GG_API

class KeywordResearchView(LoginRequiredMixin, View):
    def get(self, request):
        
        context = {
            'country_data': DF_GG_API.COUNTRY_LIST,
            'language_data': DF_GG_API.get_language('2704'),
        }
        template = 'app_market_explorer/keyword_research.html'
        return render(request, template_name=template, context=context)