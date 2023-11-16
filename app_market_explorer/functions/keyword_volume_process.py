from .. import models
from django.db.models import Q
import datetime

def volume_obj_create(root_key_qs, serp_config):

    exit_vol_qs = models.KeywordVolumeModel.objects.filter(Q(keyword__in=root_key_qs)&Q(config=serp_config)).select_related('keyword')

    exit_vol_on_update = exit_vol_qs.filter(on_update=True) #
    exit_vol_nearly_update = exit_vol_qs.filter(update_time__month=datetime.datetime.now().month)

    new_vol_qs = []
    new_keyword = root_key_qs.exclude(id__in=[item.keyword.id for item in exit_vol_qs])