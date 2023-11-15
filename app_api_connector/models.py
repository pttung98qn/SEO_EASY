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
	task_id = models.CharField(max_length=75)
	post_data = models.JSONField()
	res_data = models.JSONField()
	res_status_code = models.IntegerField()
	status_code = models.IntegerField()
	