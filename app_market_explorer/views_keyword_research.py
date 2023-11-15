from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin

class KeywordResearchView(LoginRequiredMixin, View):
    def get(self, request):
        template = 'app_market_explorer/keyword_research.html'
        return render(request, template_name=template)