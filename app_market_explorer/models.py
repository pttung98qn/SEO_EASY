from django.db import models
from django.contrib.auth.models import User
from app_api_connector.dataforseo import gg_api as DFS_GG_API

COUNTRY_OPTION = [(str(item['location_code']),item['location_name']) for item in DFS_GG_API.COUNTRY_LIST]
LOCATION_OPTION = [(str(item['location_code']),item['location_name']) for item in DFS_GG_API.LOCATION_LIST]
LANGUAGE_OPTION = [(item['language_code'],item['language_name']) for item in DFS_GG_API.LANGUAGE_LIST]
SE_DOMAIN_OPTION = [(item['search_domain'],item['search_domain']+'('+item['country']+')') for item in DFS_GG_API.SEARCH_ENGINE_LIST]
DEVICE_OPTION = [('mb','Mobile'), ('dk','Desktop')]

# Create your models here.

class SerpConfigModel(models.Model):
	country_code = models.CharField(max_length=10 ,choices=COUNTRY_OPTION)
	location_code = models.CharField(max_length=10, choices=LOCATION_OPTION, null=True, blank=True)
	language_code = models.CharField(max_length=10, choices=LANGUAGE_OPTION, null=True, blank=True)
	device = models.CharField(max_length=5, choices=DEVICE_OPTION)
	se_domain = models.CharField(max_length=25, choices=SE_DOMAIN_OPTION)

	class Meta:
		verbose_name = 'Serp Config'
	def __str__(self):
		country = self.get_country_code_display()
		location = self.location_code if self.location_code else ''
		language = self.language_code if self.language_code else ''
		se_domain = self.se_domain.replace('google.','')
		return f'{country}_{location}_{language}_{self.device}_{se_domain}'
	
class KeywordAnalysisModel(models.Model):
	name = models.CharField(max_length=125)

	status = models.CharField(max_length=25, default='running') #running/ done/ error

	project = models.IntegerField(null=True, blank=True)
	keyword_count = models.IntegerField(default=0)
	serp_config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	summary = models.JSONField(null=True, blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Keyword Analysis'
	def __str__(self):
		return self.name

class Keyword_KA_Model(models.Model):
	keyword = models.CharField(max_length=125)
	analytics_group = models.ForeignKey(KeywordAnalysisModel, on_delete=models.CASCADE)

	volume = models.IntegerField(null=True, blank=True)
	trend = models.IntegerField(null=True, blank=True)
	volume_history = models.JSONField(null=True, blank=True)
	serp = models.IntegerField(null=True, blank=True)
	kd = models.IntegerField(null=True, blank=True)
	avr_cpc = models.FloatField(null=True, blank=True)
	

	last_update_kd = models.DateTimeField(null=True, blank=True)
	last_update_volume = models.DateTimeField(null=True, blank=True)
	last_update_serp = models.DateTimeField(null=True, blank=True)

	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Keyword'
	def __str__(self):
		return self.root
	
class KeywordRootModel(models.Model):
	keyword = models.CharField(max_length=125, db_index=True, unique=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Keyword Root'
	def __str__(self):
		return self.keyword

class KeywordVolumeModel(models.Model):
	keyword = models.ForeignKey(KeywordRootModel, on_delete=models.CASCADE)
	config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	volume = models.IntegerField(null=True, blank=True)
	volume_history = models.JSONField(null=True, blank=True)
	trend = models.IntegerField(null=True, blank=True)
	avr_cpc = models.FloatField(null=True, blank=True)
	on_update = models.BooleanField(default=False)
	udpate_time = models.DateTimeField(auto_now=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Keyword Info'
	def __str__(self):
		return self.keyword.keyword

class KeywordKDModel(models.Model):
	keyword = models.ForeignKey(KeywordRootModel, on_delete=models.CASCADE)
	config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	kd = models.IntegerField(null=True, blank=True)
	on_update = models.BooleanField(default=False)
	udpate_time = models.DateTimeField(auto_now=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Keyword Info'
	def __str__(self):
		return self.keyword.keyword

class KeywordSerpModel(models.Model):
	task_id = models.CharField(max_length=45)
	config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	push = models.BooleanField(default=False)
	get = models.BooleanField(default=False)

	keyword = models.ForeignKey(KeywordRootModel, on_delete=models.CASCADE)
	main_intent = models.CharField(max_length=5, null=True, blank=True)
	intent_info = models.JSONField(max_length=50, null=True, blank=True)

	check_url = models.CharField(max_length=225, null=True, blank=True)
	item_types = models.CharField(max_length=555)
	se_results_count = models.IntegerField()
	top_10 = models.JSONField(null=True, blank=True)
	full_serp_data = models.JSONField(null=True, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Serp'
	def __str__(self):
		return self.keyword


class DomainModel(models.Model):
	domain = models.CharField(max_length=255, db_index=True)

	class Meta:
		verbose_name = 'Domain'
	def __str__(self):
		return self.domain
	

class KDOrderModel(models.Model):
	from_action = models.CharField(max_length=75)
	id_main = models.IntegerField()

	status = models.CharField(default='created', max_length=15) #created / pushed / done / error
	
	list_obj = models.JSONField()
	order_count = models.IntegerField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

class VolumeOrderModel(models.Model):
	from_action = models.CharField(max_length=75)
	id_main = models.IntegerField()

	status = models.CharField(default='created', max_length=15) #created / pushed / done / error

	list_obj = models.JSONField()
	order_count = models.IntegerField()
	get_from_date = models.CharField(default='2022-06-30', max_length=15)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Volume Order'
	def __str__(self):
		return f'{self.from_action}__{self.id_main}'

class SERPOrderModel(models.Model):
	from_action = models.CharField(max_length=75)
	id_main = models.IntegerField()

	status = models.CharField(default='created', max_length=15) #created / pushed / done / error

	list_obj = models.JSONField()
	order_count = models.IntegerField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'SERP Order'
	def __str__(self):
		return f'{self.from_action}__{self.id_main}'

class KeywordResearchOrderModel(models.Model):
	keyword = models.CharField(max_length=80)
	config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	
	filter_include = models.TextField(null=True, blank=True)
	filter_exclude = models.TextField(null=True, blank=True)
	filter_volume_min = models.IntegerField(null=True, blank=True)
	filter_volume_max = models.IntegerField(null=True, blank=True)

	status = models.CharField(default='created', max_length=15) #created / pushed / done / error
	request_num = models.IntegerField(default=0)
	total_count = models.IntegerField(default=0)
	total_result = models.IntegerField(default=0)
	total_cost = models.IntegerField(default=0)
	total_credit = models.IntegerField(default=0)

	cache_total_vol = models.IntegerField(null=True, blank=True)
	cache_total_prev_vol = models.IntegerField(null=True, blank=True)
	cache_vol_history = models.JSONField(null=True, blank=True)
	cache_kd = models.CharField(max_length=25)

	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Keyword research Order'
	def __str__(self):
		return f'{self.keyword}__{self.config.id}'
	
class Keyword_RS_Model(models.Model):
	keyword = models.CharField(max_length=125)
	order = models.ForeignKey(KeywordResearchOrderModel, on_delete=models.CASCADE)
	request = models.IntegerField(default=0)
	
	volume = models.IntegerField(null=True, blank=True)
	volume_history = models.JSONField(null=True, blank=True)
	trend = models.IntegerField(null=True, blank=True)
	serp = models.IntegerField(null=True, blank=True)
	kd = models.IntegerField(null=True, blank=True)
	avr_cpc = models.FloatField(null=True, blank=True)

	create_time = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name = 'Keyword RS'
	def __str__(self):
		return self.keyword.keyword