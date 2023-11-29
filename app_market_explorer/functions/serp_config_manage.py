from .. import models
from app_api_connector.dataforseo import gg_api as DF_GG_API

def serp_config(country, location, device, language_code, se_domain):
    serp_config_obj = models.SerpConfigModel.objects.filter(
            country_code=country,
            location_code=location,
            device = device,
            language_code = language_code,
            se_domain = se_domain
        )
    if serp_config_obj.exists():
        return serp_config_obj[0]
    else:
        new_config = models.SerpConfigModel.objects.create(
            country_code=country,
            location_code=location,
            device = device,
            language_code = language_code,
            se_domain = se_domain
        )
        return new_config

def keyword_analytics_config(country, language_code):
    device = 'mb'
    se_domain = 'google.com'
    location = None
    return serp_config(country, location, device, language_code, se_domain)