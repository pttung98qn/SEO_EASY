from django.contrib.auth.signals import user_logged_in, user_logged_out
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from . import models
from .functions import user_info


@receiver(user_signed_up)
def user_signed_up_handler(sender, request, user, **kwargs):
    print(f"User {user.username} has successfully signed up.")
    models.CustomerModel.objects.create(
        user = user
    )


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if '/admin/' in request.get_full_path():
        return 0
    ip = user_info.get_client_ip(request)
    models.LoginLogModel.objects.create(
        user=user,
        ip = ip,
        user_agents = request.user_agent,
        location = user_info.ipgeolocation(ip),
        device = user_info.get_device(request.user_agent)
    )
    user.customermodel.online = True
    user.customermodel.save()

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    # Xử lý khi người dùng đăng xuất
    print(f"User {user.username} logged out.")
    user.customermodel.online = False
    user.customermodel.save()