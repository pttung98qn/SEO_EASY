from django.db.models import Q
from django.utils import timezone

from app_api_connector import models as api_c_models
from app_api_connector.dataforseo import gg_api as DF_GG_API
from app_system.functions import error_handle
import time, json

from .. import models
from . import keyword_manage

def research_filter(exclude, include, min_volume, max_volume):
	filters = []
	
	if min_volume and max_volume:
		vol_filter = ['keyword_info.search_volume','in',[min_volume, max_volume]]
	else:
		if min_volume:
			vol_filter = ['keyword_info.search_volume','>=',min_volume]
		elif max_volume:
			vol_filter = ['keyword_info.search_volume','<=',max_volume]
		else:
			vol_filter = None

	if vol_filter:
		if len(filters)>=1:
			filters.append('and')
		filters.append(vol_filter)
	if exclude:
		exclude = exclude.split(',')
		for item in exclude[:5]:
			if item!='':
				if len(filters)>=1:
					filters.append('and')
				filters.append(['keyword', 'not_like', f'%{item}%'])

	if include:
		include = include.split(',')
		if len(filters)>=1:
			filters.append('and')
		key_list = '|'.join(include)
		filters.append(['keyword', 'regex', f'({key_list})'])

	return filters if filters else None

def keyword_research_request(order, new_request, config=None, include_seed_keyword=None):
	start_time = time.time()

	offset = new_request.offset
	if not include_seed_keyword:
		include_seed_keyword = True if offset ==0 else False

	if not config:
		config = order.config
	filters = research_filter(order.filter_exclude, order.filter_include, order.filter_volume_min, order.filter_volume_max)
	res = DF_GG_API.keyword_suggestions(keyword = order.keyword, include_seed_keyword = include_seed_keyword, location_code = config.country_code, language_code = config.language_code, filters = filters)
	if res.status_code != 200:
		new_request.status='error'
		new_request.res_data = {
			'status_code':res.status_code
		}
		error_handle.error_save("research keyword error", traceback=f"API response code {res.status_code}", send_mail=True)
	else:
		data = json.loads(res.text)
		new_request.res_data = data
		
		if data['status_code'] not in [20000,20100]:
			new_request.status='error'
			error_handle.error_save("research keyword error", traceback=data, send_mail=True)
		else:
			new_request.status='success'

	end_time = time.time()
	new_request.turnarround_time = int(end_time - start_time)
	new_request.save()

	return {
		'order':order,
		'new_request':new_request,
	}

def create_rs_keyword(root_key_list, order, request, keyword_data):
	list_obj = []
	exit_key = models.Keyword_RS_Model.objects.filter(Q(keyword__in=root_key_list)&Q(order=order)).values_list('keyword', flat=True)
	for key in root_key_list:
		if key not in exit_key:
			key_data = keyword_data[key.keyword]

			volume_history = key_data['keyword_info']['monthly_searches']
			search_volume = keyword_manage.get_vol(key_data['keyword_info']['search_volume'], volume_history)
			new_obj = models.Keyword_RS_Model(
				order = order,
				request = request.id,
				keyword = key.keyword,
				kd = key_data['keyword_properties']['keyword_difficulty'],
				volume = search_volume['search_volume'],
				volume_history = volume_history,
				trend = search_volume['vol_change'],
				avr_cpc = key_data['keyword_info']['cpc']
			)
			list_obj.append(new_obj)
	new_obj = models.Keyword_RS_Model.objects.bulk_create(list_obj)
	return new_obj

def keyword_result_process(order, new_request):
	data = new_request.res_data
	new_request.cost = data['cost']
	
	order.total_cost+=data['cost']

	result =  data['tasks'][0]['result']
	if result:
		new_request.offset_token = result[0]['offset_token']

		item_list = result[0]['items']
		key_data_as_dict = dict(())
		for item in item_list:
			key_data_as_dict[item['keyword']]=item

		keyword_list = [item['keyword'] for item in item_list]
		root_key_data = keyword_manage.root_keyword_create(keyword_list)
		set_root_key = root_key_data['set_keyword']
		root_key_qs = models.KeywordRootModel.objects.filter(keyword__in=list(set_root_key))
		
		keyword_manage.volume_create(root_key_qs, order.config, key_data_as_dict)
		keyword_manage.kd_create(root_key_qs, order.config, key_data_as_dict)
		create_rs_keyword(root_key_qs, order, new_request, key_data_as_dict)


	new_request.total_count = result[0]['total_count'] if result else 0
	new_request.items_count = result[0]['items_count'] if result else 0
	new_request.cost = data['cost']
	new_request.save()


def get_old_order(order, offset, config=None):
	if not config:
		config = order.config
	old_order = models.KeywordResearchOrderModel.objects.filter(
		Q(keyowrd=order.keyword)&Q(location_code=config.country_code)&Q(language_code=config.language_code)
	)

	seven_days_ago = timezone.now() - timezone.timedelta(days=7)
	old_order = old_order.filter(create_time__date__gte=seven_days_ago.date()).order_by('-id').first()

	if not old_order.exist():
		return None 
	
	old_order_full = old_order.filter()

	old_request = api_c_models.KeywordResearchRequest.objects.filter(
		Q(id__in=old_order)&Q(offset=offset)
	)

def order_run(order, new_request, config=None):
	if not config:
		config = order.config

	old_order = get_old_order(order, new_request.offset)
	if old_order:
		new_request.copy = True
		new_request.res_data = old_order.res_data
		new_request.save()
	else:
		output = keyword_research_request(order, new_request, config=config, include_seed_keyword=None)
	

def order_first_push(order, config):
	new_request = api_c_models.KeywordResearchRequest.objects.create(
		order = order.id,
		offset = 0,
		creator = order.creator
	)

	keyword_research_request(order, new_request, config=config, include_seed_keyword=None)





	