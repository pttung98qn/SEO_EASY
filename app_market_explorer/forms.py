from django import forms
from . import models

class KeywordAnalysisForm(forms.Form):
    project_name = forms.CharField(max_length=125)
    country_code = forms.CharField(max_length=10, widget=forms.Select(choices=models.COUNTRY_OPTION))
    language_code = forms.CharField(max_length=10, required=False, widget=forms.Select(choices=models.LOCATION_OPTION))
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