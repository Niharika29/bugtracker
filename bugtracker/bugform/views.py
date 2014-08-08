from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
import pygeoip
from bugform.forms import BugForm, AdminForm, SimpleTable
from bugform.models import BugModel, AdminModel
import django_tables2 as tables 
from django_tables2 import RequestConfig
from ipware.ip import get_ip

def admin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			q = BugModel.objects.all()
			table = SimpleTable(q)
			RequestConfig(request).configure(table)
			return render(request, 'bugreports.html', {'table':table} )
		else:
			return HttpResponse('You are dead!')
		
	form = AdminForm()
	return render(request, 'adminform.html', { 'form': form, })
	
def index(request):
	if request.method == 'POST':
		form = BugForm(request.POST)
		if form.is_valid():
			form.save()
			template = 'postform.html'
			return render(request, template)

	else:
		ip = get_ip(request)
		geocity = pygeoip.GeoIP('GeoLiteCity.dat')
		city = geocity.record_by_addr('ip')
		data = {'ip':ip, 
			'city': city['city'],
			'country': city['country_name'],
			'timezone': city['time_zone'] 
		}
		
		form = BugForm(initial=data)
		
	return render(request, 'data.html', { 'form': form, })
	
def getip(request):
	xforwardedfor = request.META.get('HTTP_X_FORWARDED_FOR')
	if xforwardedfor:
		ip = xforwardedfor.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR') 
	return ip
	
def bug_edit(request, pk):
	if request.method == 'POST':
		record = BugModel.objects.get(pk=pk)
		form = BugForm(request.POST, instance=record)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../../admin')

	else:
		record = BugModel.objects.get(pk=pk)
		data = {
			'date':record.date,
			'email': record.email,
			'desc': record.desc,
			'os': record.os,
			'browser': record.browser,
			'loadtime': record.loadtime,
			'ip': record.ip, 
			'city': record.city,
			'country': record.country,
			'timezone': record.timezone,
			'netspeed': record.netspeed,
			'bugstatus': record.bugstatus,
			'bugpriority': record.bugpriority
		}
		
		form = BugForm(initial=data)
	return render(request, 'editbugform.html', { 'form': form, })
	
def bug_delete(request, pk):
	record = BugModel.objects.get(pk=pk)
	record.delete()
	return HttpResponseRedirect('../../admin')
		
