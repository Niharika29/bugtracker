from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.gis.utils import GeoIP
import pygeoip

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
	geocountry = pygeoip.GeoIP('GeoIP.dat')
	geocity = pygeoip.GeoIP('GeoLiteCity.dat')
	country = geocountry.country_code_by_addr('122.161.236.2')
	city = geocity.record_by_addr('122.161.236.2')
	context = { 'name':name, 'email':email, 'bug':bug, 'ip':ip, 'country':country, 'city':city }
	
	return render(request, template, context)
