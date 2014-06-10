from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import render_to_response
import json

from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from projects.models import Friends, UserProfile, PersonInProject, Task, Project
from tasker.forms import UserProfileForm
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

def logout_view(request):
	context = RequestContext(request)
	logout(request)
	return render_to_response('login.html', {'logout': True}, context)

def settings(request):
	try:
		u = request.user
	except User.DoesNotExist:
		return HttpResponseNotFound('<h1>User not found</h1>')

	if request.method == "POST" and request.is_ajax():
		ok, opt = __settings(u, request)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('settings.html')
		context = RequestContext(request, {'data_page_type': 'friends'})
		return HttpResponse(template.render(context))

def __settings(user, request):
	# print(request.POST)
	form = UserForm(request.POST)
	if form.is_valid():
		print("działa")
		user.username = form.cleaned_data['username']
		user.password = form.cleaned_data['password']
		user.email = form.cleaned_data['email']
		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save(False,True)
		return True, {}
	else:
		print("coś nie idzie")
		return False, list(form.errors.keys()) if form.errors else None

def public_profile(request, id):
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
	can_edit = False
	if id == request.user.id:
		can_edit = True
	context = RequestContext(request, {
		'current_user': current_user,
		'current_profile': current_user.get_profile(),
		'project': project,
		'task': task,
		'data_page_type': 'friends',
		'can_edit': can_edit,
		'add': False
	})
	return HttpResponse(template.render(context))

def user_profile(request):
	user_id = request.user.id
	print("user_profile")
	return public_profile(request, user_id)

def profile_edit(request):
	try:
		p = request.user.get_profile()
	except UserProfile.DoesNotExist:
		return HttpResponseNotFound('<h1>Profile not found</h1>')

	if request.method == "POST" and request.is_ajax():
		ok, opt = __profile_edit(p, request)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('profile_write.html')
		context = RequestContext(request, {
			'profile': p,
			'genders': UserProfile.GENDERS,
			'data_page_type': 'friends',
		})
		return HttpResponse(template.render(context))

def __profile_edit(profile, request):
	# print(request.POST)
	form = UserProfileForm(request.POST)
	if form.is_valid():
		print("to działa")
		profile.gender = form.cleaned_data['gender']
		print(profile.gender)
		profile.birthdate = form.cleaned_data['birthdate']
		profile.save(False,True)
		return True, {}
	else:
		return False, list(form.errors.keys()) if form.errors else None

def friends_list(request):
	userId = request.user.id
	peopleIds = Friends.objects.filter(user1Id=userId).values('user2Id').distinct()
	print(peopleIds)
	people = User.objects.filter(id__in=peopleIds)
	template = loader.get_template('friend_list.html')
	context = RequestContext(request, {
		'people': people,
		'redirect': 'public_profile'
		})
	return HttpResponse(template.render(context))

def friends_edit(request):
	userId = request.user.id
	peopleIds = Friends.objects.exclude(user1Id=userId).values('user2Id').distinct()
	people = User.objects.filter(id__in=peopleIds)
	people = User.objects.all()
	template = loader.get_template('friend_list.html')
	context = RequestContext(request, {
		'people': people,
		'add': True
		})
	return HttpResponse(template.render(context))

def friends_add(request, id):
	context = RequestContext(request)
	new_friend = User.objects.filter(id=id)[0]
	friendship = Friends(user1Id=request.user, user2Id=new_friend)
	friendship.save()
	return HttpResponseRedirect('friend_list')
