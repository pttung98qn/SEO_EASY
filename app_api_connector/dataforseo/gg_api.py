import json, requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent

default_auth = HTTPBasicAuth('pmm23.gasistant@gmail.com', 'd7146b960c5d44da')

with open(BASE_DIR/'gg_language.json', 'r') as f:
	FULL_LANGUAGE = json.load(f)['data']

with open(BASE_DIR/'gg_search_engine.json', 'r') as f:
	SEARCH_ENGINE = json.load(f)['data']

with open(BASE_DIR/'gg_location.json', 'r') as f:
	FULL_LOCATION = json.load(f)['data']

with open(BASE_DIR/'gg_location_and_language.json', 'r') as f:
	LANGUAGE_LOCATION = json.load(f)['data']

SEARCH_ENGINE_LIST = sorted(SEARCH_ENGINE, key=lambda d: d['search_domain'])
LANGUAGE_LIST = sorted(FULL_LANGUAGE, key=lambda d: d['language_name'])
LOCATION_LIST = sorted(FULL_LOCATION, key=lambda d: d['location_name'])
COUNTRY_LIST = sorted([
		{'location_name':line['location_name'],'location_code':line['location_code']} for line in LANGUAGE_LOCATION
	], key=lambda d: d['location_name'])


LANGUAGE_LOCATION_DICT = dict(())
for line in LANGUAGE_LOCATION:
	LANGUAGE_LOCATION_DICT[str(line['location_code'])] = {
		'location_name': line['location_name'],
		'country_iso_code': line['country_iso_code'],
		'available_languages':line['available_languages']
	}
LOCATION_DICT = dict(())
for line in LOCATION_LIST:
	parrent = str(line['location_code_parent'])
	if not parrent:
		LOCATION_DICT[parrent] = []
	else:
		if parrent not in LOCATION_DICT:
			LOCATION_DICT[parrent] = []
		LOCATION_DICT[parrent].append({
			"location_code": line['location_code'],
			"location_name": line['location_name'],
			"country_iso_code": line['country_iso_code'],
		})
	
def get_language(country_code, all_option=False):
	country_code = str(country_code)
	if country_code in LANGUAGE_LOCATION_DICT:
		data = LANGUAGE_LOCATION_DICT[country_code]['available_languages']
		data = sorted(data, key=lambda d: d['keywords'], reverse=True)
	else:
		data = []
	if all_option and len(data)>=2:
		data.insert(0, {
			'language_name':'All',
			'language_code':'',
		})
	return data

def get_sub_location(country_code):
	return LOCATION_DICT[country_code]


def serp_post(order_data, domain, location, language, device,
				priority=None, se_domain=None, postback_data="regular", postback_url=None, pingback_url=None):
	'''
		Requests serp data from dataforseo & get back data by postback_url
		*****
		keywords_list (list of string): 
		priority (int): 1-standard (0.6$/ 1k task), 2-high priority(1.2$/ 1k task) (1 key request = 1 task)
		location_code (int): data in './location_code.json'
		language_code (str): data in './language_code.json'
		search_engine_domain (str): data in './se_domain.json' (default=None => auto set follow location code)
		device (str): desktop/mobile
		tag (str): tag of task
		postback_url (url): API to post back data on server
		postback_data(str): regular, advanced, html ( Type of sesults)
	'''
	end_point = "https://api.dataforseo.com/v3/serp/google/organic/task_post"
	post_data = dict()
	index = 0
	for order in order_data:
		order_id = order['id']
		if not priority:
			priority = 3

		post_data[len(post_data)] = {
			'keyword': order['keyword__keyword'],
			'priority': priority,
			'location_code':location,
			'language_code':language,
			'device':device,
			'tag': f'{domain}_{order_id}'
		}
		if se_domain:
			post_data[index]['se_domain'] = se_domain
		if postback_url:
			post_data[index]['postback_url'] = postback_url
			post_data[index]['postback_data'] = postback_data
		if pingback_url:
			post_data[index]['pingback_url'] = pingback_url
		index = index+1

	res = requests.post(end_point, json = post_data, auth = default_auth)
	return res

def volume_api(order, keyword_list, tag, location_code, date_from):
	end_point = 'https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/task_post'
	post_data = dict()
	post_data[len(post_data)] = dict(
		location_code=location_code,
		keywords = keyword_list,
		date_from = date_from,
		tag = tag,
		pingback_url = f"{settings.HOME_URL}/serp/volume-ping-back/?tag={order.id}"
	)
	res = requests.post(end_point, json = post_data, auth = default_auth)
	return res

def getback_data(task_id, api_name, option=None):
	'''
		task_id (str):
		api_name (str): volume / serp
		option (str): advanced / html/ Regular (Chỉ dành cho task "serp" )
	'''
	if api_name == 'volume':
		path = '/keywords_data/google_ads/search_volume/task_get/'
	elif api_name == 'serp':
		if not option:
			return None
		path = f'/serp/google/organic/task_get/{option}/'
	
	end_point = f"https://api.dataforseo.com/v3{path}{task_id}"
	res = requests.get(end_point, auth = default_auth)
	return res

def get_tasks_ready(api_name):
	'''
		api_name: Volume/ serp
	'''
	if api_name == 'volume':
		path = '/keywords_data/google_ads/search_volume/'
	elif api_name == 'serp':
		path = '/serp/google/organic/'
	end_point = f"https://api.dataforseo.com/v3{path}tasks_ready"
	res = requests.get(end_point, auth = default_auth)
	return res


DEFAULT_LIMIT = 1000
def keyword_suggestions(keyword, include_seed_keyword=True, exact_match=False, location_code = 2704, language_code = None, include_serp_info = False, limit=DEFAULT_LIMIT, filters=None, order_by=None, offset=0):
	'''
		target (string): target domain, the domain name of the target website, the domain should be specified without https:// or www.
		location_code (integer): unique location identifier
		filters (list): array of results filtering parameters. You can add several filters at once (8 filters maximum). For more information about filters, https://docs.dataforseo.com/v3/dataforseo_labs/filters/
		default rule (list): ["relevance,desc"]
	'''
	end_point = "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live"
	if language_code and language_code!='':
		language_code = None
	post_data = dict(())
	post_data[0] = dict(
		keyword=keyword,
		include_seed_keyword = include_seed_keyword,
		exact_match = exact_match,
		location_code = location_code,
		language_code = language_code if language_code!='' else None,
		include_serp_info = include_serp_info,
		limit = limit,
		offset = offset,
		filters = filters,
		order_by = order_by,
	)
	
	for i in range(2):
		res = requests.post(end_point, json = post_data, auth = default_auth)
		print(res)
		if res.status_code==200:
			return res
	return res