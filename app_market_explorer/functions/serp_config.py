from .. import models
from app_api_connector.dataforseo import gg_api as DF_GG_API
def serp_config(country, location, device, language_code, se_domain):
    serp_config_obj = models.SerpConfig.objects.filter(
            country=country,
            location=location,
            device = device,
            language_code = language_code,
            se_domain =se_domain
        )
    if serp_config_obj.exists():
        return serp_config_obj[0]
    else:
        new_config = models.SerpConfig.objects.create(
            
        )
        return new_config

def keyword_analytics_config(country):
    language_code = DF_GG_API.get_language(country)[0]
    device = 'mb'
    se_domain = 'google.com'
    location = None
    return serp_config(country, location, device, language_code, se_domain)