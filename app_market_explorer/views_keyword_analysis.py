from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404

from app_api_connector.dataforseo import gg_api as DF_GG_API

from . import models
from .functions import serp_config_manage, keyword_analysis_process
from .forms import KeywordAnalysisForm

class KeywordAnalysisView(LoginRequiredMixin, View):
    def get(self, request):
        
        context = {
            'country_data': DF_GG_API.COUNTRY_LIST,
            'language_data': DF_GG_API.get_language('2704'),
        }
        template = 'app_market_explorer/keyword_analysis.html'
        return render(request, template_name=template, context=context)
    
    def post(self, request):
        form = KeywordAnalysisForm(request.POST)
        if not form.is_valid():
            messages.error(request, message=form.errors, extra_tags='ERROR')
            return redirect(reverse('keyword_analysis'))
        list_keyword = form.cleaned_data['list_keyword']
        language_code = form.cleaned_data['language_code']
        country_code = form.cleaned_data['country_code']
        name = form.cleaned_data['project_name']
        
        serp_config = serp_config_manage.keyword_analytics_config(country_code, language_code)

        ka_obj = models.KeywordAnalysisModel.objects.create(
            name = name,
            serp_config = serp_config.id,
            creator = request.user
        )
        keyword_analysis_process.run_analytics(list_keyword, ka_obj, request.user, serp_config)
        return redirect(reverse('keyword_analysis_item', args=[ka_obj.id]))


def get_ka_project(request):
    project_qs = models.KeywordAnalysisModel.objects.filter(creator=request.user)
    data = project_qs.values('id','name','create_time','project')

    page = request.GET.get('page', 1)
    items_per_page = 5
    paginator = Paginator(data, items_per_page)
    page_obj = paginator.get_page(page)

    template = 'app_market_explorer/elements/keyword_analysis__history.html'
    result_data = render_to_string(template, context = {'data':page_obj})
    return JsonResponse({'result_data':result_data, 'total_count':paginator.count, 'current_count': len(page_obj.object_list)})

class KeywordAnalysisResultView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            project_obj = models.KeywordAnalysisModel.objects.get(id=id)
        except:
            raise Http404()
        if project_obj.creator != request.user:
            raise PermissionDenied
        
        project_qs = models.KeywordAnalysisModel.objects.filter(creator=request.user).only('id','name')
        context = {
            'obj': project_obj,
            'project_qs':project_qs,
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
        template = 'app_market_explorer/keyword_analysis_result.html'
        return render(request, template_name=template, context=context)

