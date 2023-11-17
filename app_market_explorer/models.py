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
	location_code = models.CharField(max_length=10, null=True, blank=True, choices=LOCATION_OPTION)
	language_code = models.CharField(max_length=10, choices=LANGUAGE_OPTION)
	device = models.CharField(max_length=5, choices=DEVICE_OPTION)
	se_domain = models.CharField(max_length=25, choices=SE_DOMAIN_OPTION)

	class Meta:
		verbose_name = 'Serp Config'
	def __str__(self):
		return self.country_code
	
class KeywordAnalysisModel(models.Model):
	name = models.CharField(max_length=125)
	project = models.IntegerField(null=True, blank=True)
	serp_config = models.IntegerField()
	summary = models.JSONField(null=True, blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Keyword Analysis'
	def __str__(self):
		return self.name

class Keyword_KA_Model(models.Model):
	analytics_group = models.ForeignKey(KeywordAnalysisModel, on_delete=models.CASCADE)

	volume = models.IntegerField(null=True, blank=True)
	serp = models.IntegerField(null=True, blank=True)
	kd = models.IntegerField(null=True, blank=True)
	volume_history = models.JSONField(null=True, blank=True)
	root = models.CharField(max_length=125)

	last_update_kd = models.DateTimeField(null=True, blank=True)
	last_update_volume = models.DateTimeField(null=True, blank=True)
	last_update_serp = models.DateTimeField()

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
	vol_history = models.JSONField(null=True, blank=True)
	on_update = models.BooleanField(default=False)
	udpate_time = models.DateTimeField(auto_now=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Keyword Info'
	def __str__(self):
		return self.keyword.keyword

class VolumeOrderModel(models.Model):
	from_action = models.CharField(max_length=75)
	id_main = models.IntegerField()
	list_obj = models.JSONField()
	order_count = models.IntegerField()
	get_from_date = models.CharField(default='2022-06-30', max_length=15)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Volume Order'
	def __str__(self):
		return f'{self.from_action}__{self.id_main}'

class KeywordKDModel(models.Model):
	keyword = models.ForeignKey(KeywordRootModel, on_delete=models.CASCADE)
	config = models.ForeignKey(SerpConfigModel, on_delete=models.PROTECT)
	KD = models.IntegerField()
	on_update = models.BooleanField(default=False)
	udpate_time = models.DateTimeField(auto_now=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Keyword Info'
	def __str__(self):
		return self.keyword.keyword

class SerpModel(models.Model):
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