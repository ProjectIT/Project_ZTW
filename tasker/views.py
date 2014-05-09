from django.http import HttpResponse
from django.shortcuts import render

from django.template import loader, RequestContext

def mainpage(request):
	return render(request, 'homepage.html')

def about(request):
	return render(request, 'about.html')

def login(request):
	return render(request, 'login.html')



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
