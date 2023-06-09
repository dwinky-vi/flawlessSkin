from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from .models import User
from main.models import Order
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_old(request):
	return render(request, 'users/base.html')

def login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user:
				auth.login(request, user)
				return HttpResponseRedirect(reverse('products:index'))
		else:
			print("login", form.errors)
	else:
		form = UserLoginForm()
	context = {
		"form": form
	}
	return render(request, 'users/login.html', context)

def registration(request):
	if request.method == 'POST':
		form = UserRegistrationForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Вы успешно зарегистрировались!')
			return HttpResponseRedirect(reverse('users:login'))
		else:
			print("registration:", form.errors)
	else:
		form = UserRegistrationForm()
	context = {
		'form': form,
	}
	return render(request, 'users/registration.html', context)

@login_required
def profile(request):
	if request.method == "POST":
		form = UserProfileForm(instance=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('users:profile'))
		else:
			print("profile:", form.errors)
	else:
		form = UserProfileForm(instance=request.user)
	orders = Order.objects.filter(user=request.user)
	context = {
		'form': form,
		'orders': orders
	}
	return render(request, 'users/profile.html', context)

@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('products:index'))
