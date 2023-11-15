from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string

def c_get_connection(sender_email):
    connect_info = settings.EMAIL_ACCOUNTS[sender_email]
    return get_connection(
        host = connect_info['EMAIL_HOST'], 
        port = connect_info['EMAIL_PORT'], 
        username = connect_info['EMAIL_HOST_USER'], 
        password = connect_info['EMAIL_HOST_PASSWORD'],
        use_tls = connect_info['EMAIL_USE_TLS'],
        use_ssl = connect_info['EMAIL_USE_SSL']
    )

def s_send_mail(sender_email, subject, context, template, ReceiversList):
    connection = c_get_connection(sender_email)
    message = render_to_string(template, context)
    EmailSender = connection.username
    send_mail(subject = subject,
                message = "",
                from_email = EmailSender,
                recipient_list = ReceiversList,
                connection=connection,
                html_message=message)