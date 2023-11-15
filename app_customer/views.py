from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def new_user(request):
	users = User.objects.all()
	return render(request, 'new_user.html',{'users':users})