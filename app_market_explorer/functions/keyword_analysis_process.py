from .. import models
from django.db.models import Q

def create_ka_keyword(root_key_list, a_obj, creator):
    list_obj = []
    exit_key = models.Keyword_KA_Model.objects.filter(Q(root__in=root_key_list)&Q(analytics_group=a_obj)).values_list('root', flat=True)

    for key in root_key_list:
        if key not in exit_key:
            new_obj = models.Keyword_KA_Model(
                analytics_group = a_obj,
                root = key.keyword,
                creator = creator
            )
            list_obj.append(new_obj)
    new_obj = models.Keyword_KA_Model.objects.bulk_create(list_obj)

    return new_obj


def run_analytics(root_key_list, a_obj, creator):
    new_keyword = create_ka_keyword(root_key_list, a_obj, creator)
