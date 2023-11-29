import datetime

from .. import models
from django.db.models import Q
from . import keyword_manage

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


def create_keyword_info(model, root_key_qs, serp_config):
    exit_qs = model.objects.filter(Q(keyword__in=root_key_qs)&Q(config=serp_config)).only('id','keyword', 'config')
    if model == models.KeywordSerpModel:
        exit_qs = exit_qs.filter(create_time__date=datetime.date.today())
    exit_qs = exit_qs.select_related('keyword')

    new_list = []
    new_keyword = root_key_qs.exclude(id__in=[item.keyword.id for item in exit_qs])
    for key in new_keyword:
        new_obj = models.KeywordSerpModel(
            keyword = key,
            config = serp_config
        )
        new_list.append(new_obj)
    new_qs = models.KeywordSerpModel.objects.bulk_create(new_list)
    return {'exit_qs':exit_qs, 'new_qs':new_qs}


def prev_analytics(list_keyword, a_obj, creator, serp_config):
    root_key_list = keyword_manage.root_keyword_create(list_keyword)

    new_kd_keyword = create_ka_keyword(root_key_list, a_obj, creator)

    root_key_qs = models.KeywordRootModel.objects.filter(keyword__in=root_key_list)

    vol_obj_data = create_keyword_info(models.KeywordVolumeModel,root_key_qs, serp_config)
    kd_obj_data = create_keyword_info(models.KeywordKDModel,root_key_qs, serp_config)
    serp_obj_data = create_keyword_info(models.KeywordSerpModel,root_key_qs, serp_config)
    
    full_vol_id = [item.id for item in vol_obj_data['new_qs']]+[item.id for item in vol_obj_data['exit_qs']]
    full_kd_id = [item.id for item in kd_obj_data['new_qs']]+[item.id for item in kd_obj_data['exit_qs']]
    full_serp_id = [item.id for item in serp_obj_data['new_qs']]+[item.id for item in serp_obj_data['exit_qs']]

    models.VolumeOrderModel.objects.create(
        from_action = 'keyword_analysis',
        id_main = a_obj.id,
        list_obj = full_vol_id,
        order_count = len(full_vol_id),
        creator = creator
    )

    models.KDOrderModel.objects.create(
        from_action = 'keyword_analysis',
        id_main = a_obj.id,
        list_obj = full_kd_id,
        order_count = len(full_kd_id),
        creator = creator
    )

    models.SERPOrderModel.obj.create(
        from_action = 'keyword_analysis',
        id_main = a_obj.id,
        list_obj = full_serp_id,
        order_count = len(full_serp_id),
        creator = creator
    )







