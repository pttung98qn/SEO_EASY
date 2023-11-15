from django.db import models

# Create your models here.

class ErrorLogModel(models.Model):
	error_name = models.CharField(max_length=50)
	traceback = models.TextField(null=True, blank=True)
	error_timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Error{self.error_name} at {self.error_timestamp}"
