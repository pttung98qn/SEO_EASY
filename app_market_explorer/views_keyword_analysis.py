from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin

from app_api_connector.dataforseo import gg_api as DF_GG_API

from . import models, functions

class KeywordAnalysisView(LoginRequiredMixin, View):
    def get(self, request):
        template = 'app_market_explorer/keyword_analysis.html'

        context = {
            'range_10': range(10),
            'country_data':DF_GG_API.COUNTRY_LIST
        }
        return render(request, template_name=template, context=context)
    def post(self, request):
        data = request.POST
        country = data.get('country')
        name = data.get('project_name')
        list_keyword = data.get('list_keyword')
        serp_config = functions.serp_config_manage.keyword_analytics_config(country)
        print(serp_config)
        
        return JsonResponse({'status':'submit oke', 'data':data, 'serp_config':serp_config})
    
class KeywordAnalysisResultView(LoginRequiredMixin, View):
    def get(self, request, id):
        template = 'app_market_explorer/keyword_analysis_result.html'
        context = {
            'range_10': range(10),
            'competitors':[{
                    'domain':'domain1.com',
                    'mk_share': 25,
                    'mk_share_p': 100,
                },
                {
                    'domain':'domain2.com',
                    'mk_share': 20,
                    'mk_share_p': 80,
                },
                {
                    'domain':'domain3.com',
                    'mk_share': 15,
                    'mk_share_p': 60,
                },
                {
                    'domain':'domain4.com',
                    'mk_share': 10,
                    'mk_share_p': 50,
                },
                {
                    'domain':'domain5.com',
                    'mk_share': 7,
                    'mk_share_p': 10,
                },
                {
                    'domain':'domain6.com',
                    'mk_share': 4,
                    'mk_share_p': 5,
                },
                {
                    'domain':'domain7.com',
                    'mk_share': 3,
                    'mk_share_p': 3,
                },
                {
                    'domain':'domain8.com',
                    'mk_share': 2,
                    'mk_share_p': 2,
                },
                {
                    'domain':'domain9.com',
                    'mk_share': 2,
                    'mk_share_p': 2,
                },
                {
                    'domain':'domain10.com',
                    'mk_share': 1,
                    'mk_share_p': 1,
                }
            ]
        }
        return render(request, template_name=template, context=context)

