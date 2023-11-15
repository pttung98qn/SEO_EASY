from . import views, views_keyword_research, views_keyword_analysis
from django.urls import path

urlpatterns = [
    path('keyword-research/', views_keyword_research.KeywordResearchView.as_view(), name='keyword_research'),
    path('keyword-analysis/', views_keyword_analysis.KeywordAnalysisView.as_view(), name='keyword_analysis'),
    path('keyword-analysis/<int:id>/', views_keyword_analysis.KeywordAnalysisResultView.as_view()),
]