from .. import models
from django.db.models import Q
import datetime

def volume_obj_create(root_key_qs, serp_config):
    exit_vol_qs = models.KeywordVolumeModel.objects.filter(Q(keyword__in=root_key_qs)&Q(config=serp_config)).select_related('keyword')
    new_vol_qs = []
    new_keyword = root_key_qs.exclude(id__in=[item.keyword.id for item in exit_vol_qs])
    for key in new_keyword:
        new_obj = models.KeywordVolumeModel(
            keyword = key,
            config = serp_config
        )
        new_vol_qs.append(new_obj)
    new_obj = models.KeywordVolumeModel.objects.bulk_create(new_vol_qs)
    return {'exit_vol_qs':exit_vol_qs, 'new_vol_qs':new_obj}