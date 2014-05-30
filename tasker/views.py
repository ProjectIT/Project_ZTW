from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from projects.models import UserProfile
import datetime

def mainpage(request):
	return render(request, 'homepage.html')

def about(request):
	return render(request, 'about.html')

def loginSite(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		if 'login-submit' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				# the password verified for the user
				if user.is_active:
					login(request, user)
					print("User is valid, active and authenticated")
					return HttpResponseRedirect('profile/' + str(user.id))
				else:
					print("The password is valid, but the account has been disabled!")
			else:
				# the authentication system was unable to verify the username and password
				print("The username and password were incorrect.")
		elif 'register-submit' in request.POST:
			username = request.POST['register-username']
			email = request.POST['register-email']
			password = request.POST['register-password']
			user = User.objects.create_user(username, email, password)
			user.save()
			user.set_password(password)
			user.save()
			registerDate = datetime.datetime.now()
			userProfile = user.get_profile()
			userProfile.save()
			registered = True
	return render_to_response('login.html', {'registered': registered}, context)

def settings(request):
	return render_to_response('login.html', context)

def public_profile(request, id):
	template = loader.get_template('friend_read.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))


def friends_list(request, id):
	template = loader.get_template('friend_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))
