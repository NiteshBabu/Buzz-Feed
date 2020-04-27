from django.shortcuts import render, redirect
from .form import UserRegister, UserUpdate, ProfileUpdate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegister(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Account Created For {username}, Please Sign In..!!')
			return redirect('login')
	else:
		form = UserRegister()
	
	return render(request, "users/register.html", {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':		
		u_form = UserUpdate(request.POST, instance = request.user)  			  # we pass the instance to populate the fields because it's model form
		p_form = ProfileUpdate(request.POST, request.FILES, instance = request.user.profile)   # we pass the instance to populate the fields because it's model form
		
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Successfully Updated....!')
			return redirect('profile')
	else:
		u_form = UserUpdate(instance = request.user)
		p_form = ProfileUpdate(instance = request.user.profile)
	
	context = {
		'title' : 'Profile',
		'u_form' : u_form,
		'p_form' : p_form
	}	
	return render(request, 'users/profile.html', context)


class UserLoginView(LoginView):
	
	model : User
	# print(dir(LoginView))
	redirect_authenticated_user = '/cool'
	



