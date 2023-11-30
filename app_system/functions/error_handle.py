from .. import models
from .email_process import s_send_mail

def error_save(error_name, traceback=None, send_mail=False):
	models.ErrorLogModel.objects.create(
		error_name=error_name,
		traceback = traceback
	)
	if send_mail:
		subject = '[SEO REPORTER ERROR] Phát hiện lỗi'
		context = {
			'name': 'error_name',
			'traceback':traceback,
		}
		template = 'app_system/error_alert_mail.html'
		s_send_mail('pttung98.qn@gmail.com', subject, context, template, ['pmm23.gasistant@gmail.com'])