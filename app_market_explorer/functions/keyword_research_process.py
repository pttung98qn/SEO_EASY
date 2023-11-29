from app_api_connector import models as api_c_models
from app_api_connector.dataforseo import gg_api as DF_GG_API
from app_system.functions import error_handle
import time, json

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
		filters.append(vol_filter)

	if include:
		if len(filters)>=1:
			filters.append('and')
		key_list = '|'.join(include)
		filters.append(['keyword', 'regex', f'({key_list})'])

	if exclude:
		for item in exclude[:5]:
			if item!='':
				filters.append('and')
				filters.append(['keyword', 'not_like', f'%{item}%'])
	return filters

def keyword_success(order, new_request, include_seed_keyword=None):
	start_time = time.time()

	offset = new_request.offset
	if not include_seed_keyword:
		include_seed_keyword = True if offset ==0 else False

	filters = research_filter(order.filter_exclude, order.filter_include, order.filter_volume_min, order.filter_volume_max)
	res = DF_GG_API.keyword_suggestions(keyword = order.keyword,include_seed_keyword = include_seed_keyword,location_code = order.location_code,language_code = order.language_code,filters = filters)
	result = None
	if res.status_code != 200:
		new_request.status='error'
		new_request.res_data = {
			'status_code':res.status_code
		}
		error_handle.error_save("research keyword error", error_message=f"API response code {res.status_code}", send_mail=True)
	else:
		data = json.loads(res.text)
		if data['status_code'] not in [20000,20100]:
			error_handle.error_save("research keyword error", error_message=f"API response code "+str(data['status_code']), send_mail=True)
		else:
			result =  data['tasks'][0]['result']
	if result and result[0]['items']:
		keyword_list = []
		for item in result[0]['items']:
			volume_history = item['keyword_info']['monthly_searches']
			
		

	end_time = time.time()
	elapsed_time = end_time - start_time


def request_push(order, offset):
	new_request = api_c_models.KeywordResearchRequest.objects.create(
		order = order.id,
		offset = 0
	)

	