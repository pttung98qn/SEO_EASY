from django.db.models import Q

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

	new_key_list = models.KeywordRootModel.objects.bulk_create(list_new_obj)
	return {
		'set_keyword':set_keyword,
		'exist_key_qs':exist_key_qs,
		'new_key_list':new_key_list
	}



def get_vol(search_volume, volume_history):
	def vol_round(vol):
		lam_tron = 10
		if vol>100000:
			lam_tron = 1000
		elif vol>1000:
			lam_tron = 100
		vol = round(vol/lam_tron)*lam_tron
		return vol
	
	if volume_history:
		search_volume = sum([item['search_volume'] for item in volume_history[:3]])/3
		prev_search_volume = sum([item['search_volume'] for item in volume_history[3:6]])/3
	
	else:
		search_volume = search_volume if search_volume else 0
		prev_search_volume = 0
	
	vol_change = search_volume - prev_search_volume

	if prev_search_volume == 0:
		if vol_change>0:
			vol_change = 100
		else:
			vol_change =0
	else:
		vol_change = round(vol_change/prev_search_volume*100)


	return {
		'search_volume':vol_round(search_volume), 
		'prev_search_volume': vol_round(prev_search_volume), 
		'vol_change': int(vol_change)
	}

def volume_create(root_key_qs, config, keyword_data):

	exist_list = models.KeywordVolumeModel.objects.filter(Q(keyword__in=root_key_qs)&Q(config=config)).select_related('keyword')
	for obj in exist_list:
		obj_data = keyword_data[obj.keyword.keyword]

		volume_history = obj_data['keyword_info']['monthly_searches']
		search_volume = get_vol(obj_data['keyword_info']['search_volume'], volume_history)

		obj.volume = search_volume['search_volume']
		obj.volume_history = volume_history
		obj.trend = search_volume['vol_change']
		obj.avr_cpc = obj_data['keyword_info']['cpc']
	
	models.KeywordVolumeModel.objects.bulk_update(exist_list, ['volume','volume_history', 'trend', 'avr_cpc'])

	no_vol_keyword = root_key_qs.exclude(id__in=[item.keyword.id for item in exist_list])
	new_list = []
	for obj in no_vol_keyword:
		obj_data = keyword_data[obj.keyword]
		volume_history = obj_data['keyword_info']['monthly_searches']
		search_volume = get_vol(obj_data['keyword_info']['search_volume'], volume_history)

		new_list.append(models.KeywordVolumeModel(
			keyword = obj,
			config = config,
			volume = search_volume['search_volume'],
			volume_history = volume_history,
			trend = search_volume['vol_change'],
			avr_cpc = obj_data['keyword_info']['cpc']
		))
	new_list = models.KeywordVolumeModel.objects.bulk_create(new_list)
	return {
		'exist_list':exist_list,
		'new_list':new_list
	}


def kd_create(root_key_qs, config, keyword_data):
	exist_list = models.KeywordKDModel.objects.filter(Q(keyword__in=root_key_qs)&Q(config=config)).select_related('keyword')
	for obj in exist_list:
		obj_data = keyword_data[obj.keyword.keyword]
		obj.kd = obj_data['keyword_properties']['keyword_difficulty']

	
	models.KeywordKDModel.objects.bulk_update(exist_list, ['kd'])

	no_kd_keyword = root_key_qs.exclude(id__in=[item.keyword.id for item in exist_list])
	new_list = []
	for obj in no_kd_keyword:
		obj_data = keyword_data[obj.keyword]

		new_list.append(models.KeywordKDModel(
			keyword = obj,
			config = config,
			kd = obj_data['keyword_properties']['keyword_difficulty']
		))
	new_list = models.KeywordKDModel.objects.bulk_create(new_list)
	return {
		'exist_list':exist_list,
		'new_list':new_list
	}