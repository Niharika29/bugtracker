from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.gis.utils import GeoIP

# Create your views here.

def index(request):
	myname = 'Niharika';
	template = 'data.html'
	context = { 'some_name': myname }
	return render(request, template, context)
	
def getip(request):
	xforwardedfor = request.META.get('HTTP_X_FORWARDED_FOR')
	if xforwardedfor:
		ip = xforwardedfor.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR') 
	return ip
	
def formprocess(request):
	name = 'Niharika'
	template = 'postform.html'
	email = request.POST['email']
	bug = request.POST['bug']
	ip = getip(request)
	context = { 'name':name, 'email':email, 'bug':bug, 'ip':ip }
	
	return render(request, template, context)
