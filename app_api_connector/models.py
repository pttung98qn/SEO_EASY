from django.db import models

# Create your models here.

class DFAccountModel(models.Model):
	account = models.EmailField(max_length=125)
	password = models.CharField(max_length=125)
	class Meta:
		verbose_name = 'DF Account'


	def __str__(self):
		return self.account

class DFRequestLog(models.Model):
	end_point = models.CharField(max_length=255)
	cost = models.FloatField(null=True, blank=True)
	task_id = models.CharField(max_length=75, null=True, blank=True)
	post_data = models.JSONField()
	res_data = models.JSONField(null=True, blank=True)
	res_status_code = models.IntegerField(null=True, blank=True)
	status_code = models.IntegerField(null=True, blank=True)
	
	create_time = models.DateTimeField(auto_now_add=True)
	turnarround_time = models.IntegerField(null=True, blank=True)