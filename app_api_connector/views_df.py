from django.http import JsonResponse
from .dataforseo import gg_api as DF_GG_API
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def get_language(request, search_engine, country_code):
    data = {'output':DF_GG_API.get_language(country_code)}
    return JsonResponse(data)
    