from django import forms
from . import models

class KeywordAnalysisForm(forms.Form):
    project_name = forms.CharField(max_length=125)
    country_code = forms.CharField(max_length=10, widget=forms.Select(choices=models.COUNTRY_OPTION))
    language_code = forms.CharField(max_length=10, widget=forms.Select(choices=models.LOCATION_OPTION))
    list_keyword = forms.CharField(widget=forms.Textarea)
    
    def clean_list_keyword(self):
        data = self.cleaned_data['list_keyword']
        data_list = data.replace(',','\n').split('\n')
        clean_keys = []
        for key in data_list:
            key = key.strip()
            if key !='' and len(key)<=125:
                clean_keys.append(key)
        return clean_keys

class KeywordResearchForm(forms.Form):
    keyword = forms.CharField(max_length=125)
    country_code = forms.CharField(max_length=10, widget=forms.Select(choices=models.COUNTRY_OPTION))
    language_code = forms.CharField(max_length=10, required=False, widget=forms.Select(choices=models.LOCATION_OPTION))
    filter_include = forms.CharField(widget=forms.Textarea, required=False)
    filter_exclude = forms.CharField(widget=forms.Textarea, required=False)
    filter_volume_min = forms.IntegerField(required=False)
    filter_volume_max = forms.IntegerField(required=False)

    def clean_filter_include(self):
        data = self.cleaned_data['filter_include']
        data_list = data.replace(',','\n').split('\n')
        clean_keys = []
        for key in data_list:
            key = key.strip()
            if key !='' and len(key)<=125:
                clean_keys.append(key)
        return ','.join(clean_keys[:5])
    def clean_filter_exclude(self):
        data = self.cleaned_data['filter_exclude']
        data_list = data.replace(',','\n').split('\n')
        clean_keys = []
        for key in data_list:
            key = key.strip()
            if key !='' and len(key)<=125:
                clean_keys.append(key)
        return ','.join(clean_keys[:5])
    
