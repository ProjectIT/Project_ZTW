from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from projects.models import UserProfile, PersonInProject, Task, Project
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
					print("User is valid, active and authenticated")
					return HttpResponseRedirect('profile')
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
	print("public_profile")
	template = loader.get_template('friend_read.html')
	try:
		current_user = User.objects.get(id=id)
		print(current_user)
	except User.DoesNotExist:
		return HttpResponseNotFound('<h1>User not found</h1>')
	try:
		project = PersonInProject.objects.get(userId=current_user)
	except PersonInProject.DoesNotExist:
		project = "";
	try:
		task = Task.objects.get(personResponsible=current_user)
	except Task.DoesNotExist:
		task = "";
	context = RequestContext(request, {
		'current_user': current_user,
		'project': project,
		'task': task,
		'data_page_type': 'friends'
	})
	return HttpResponse(template.render(context))

def user_profile(request):
	user_id = request.user.id
	print("user_profile")
	return public_profile(request, user_id)

def friends_list(request, id):
	template = loader.get_template('friend_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))
