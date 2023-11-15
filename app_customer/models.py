from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomerModel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	credit = models.IntegerField(default=0)
	online = models.BooleanField(default=False)
	beta_checker = models.BooleanField(default=False)
	last_visited = models.DateTimeField(null=True, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Customer Account'
	def __str__(self):
		return self.user.username

class LoginLogModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ip = models.CharField(max_length=25)
	device = models.CharField(max_length=25)
	user_agents = models.CharField(max_length=75)
	location = models.CharField(max_length=75)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Login Log'
	def __str__(self):
		return self.user.username