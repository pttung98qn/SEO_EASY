from .. import models
from .email_process import s_send_mail

def error_save(error_name, error_message=None, traceback=None, send_mail=False):
	models.ErrorLogModel.objects.create(
		error_name=error_name,
		error_message= error_message,
		traceback = traceback
	)
	if send_mail:
		subject = '[SEO REPORTER ERROR] Phát hiện lỗi'
		context = {
			'name': 'error_name',
			'error_message': error_message,
			'traceback':traceback,
		}
		template = 'app_system/error_alert_mail.html'
		s_send_mail('system@seoreporters.io', subject, context, template, ['seoreporter2022@gmail.com'])