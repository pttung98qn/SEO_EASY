from .. import models
from django.db.models import Q
from . import keyword_manage, keyword_volume_process

def create_ka_keyword(root_key_list, a_obj, creator):
    list_obj = []
    exit_key = models.Keyword_KA_Model.objects.filter(Q(root__in=root_key_list)&Q(analytics_group=a_obj)).values_list('root', flat=True)

    for key in root_key_list:
        if key not in exit_key:
            new_obj = models.Keyword_KA_Model(
                analytics_group = a_obj,
                root = key,
                creator = creator
            )
            list_obj.append(new_obj)
    new_obj = models.Keyword_KA_Model.objects.bulk_create(list_obj)
    return new_obj


def run_analytics(list_keyword, a_obj, creator, serp_config):
    root_key_list = keyword_manage.root_keyword_create(list_keyword)
    new_kd_keyword = create_ka_keyword(root_key_list, a_obj, creator)

    root_key_qs = models.KeywordRootModel.objects.filter(keyword__in=root_key_list)

    vol_obj_data = keyword_volume_process.volume_obj_create(root_key_qs, serp_config)
    full_vol_id = [item.id for item in vol_obj_data['new_vol_qs']]+[item.id for item in vol_obj_data['exit_vol_qs']]
    models.VolumeOrderModel.objects.create(
        from_action = 'keyword_analysis',
        id_main = a_obj.id,
        list_obj = full_vol_id,
        order_count = len(full_vol_id),
        creator = creator
    )


