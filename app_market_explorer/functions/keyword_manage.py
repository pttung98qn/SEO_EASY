from .. import models


def valid_key_list(list_keyword):
	clean_keys = []
	for key in list_keyword:
		key = key.strip()
		if key !='' and len(key)<=125:
			clean_keys.append(key)
	return clean_keys


def root_keyword_create(list_keyword):
	clean_keys = valid_key_list(list_keyword)
	set_keyword = set(clean_keys)
	exist_key_qs = models.KeywordRootModel.objects.filter(keyword__in=list(set_keyword))
	
	exist_key = exist_key_qs.values_list('keyword', flat=True)
	more_key = set_keyword - set(exist_key)

	list_new_obj = []
	for key in more_key:
		new_key = models.KeywordRootModel(
			keyword = key
		)
		list_new_obj.append(new_key)

	new_qs = models.KeywordRootModel.objects.bulk_create(list_new_obj)
	full_qs = new_qs.union(exist_key_qs)
	return full_qs
			
