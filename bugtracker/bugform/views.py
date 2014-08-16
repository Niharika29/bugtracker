from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import pygeoip
from bugform.forms import BugForm, AdminForm, SimpleTable, SearchForm, EditForm
from bugform.models import BugModel, AdminModel
import django_tables2 as tables 
from django_tables2 import RequestConfig
from ipware.ip import get_ip
from django.contrib.auth.decorators import login_required

def loginuser(request):
	if request.method == 'POST':
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return admin(request)
		else:
			return HttpResponse('You are dead!')
	if request.user.is_authenticated() and request.method == 'GET':
		return admin(request)
	else:
		form = AdminForm()
		return render(request, 'adminform.html', {'form': form})

@login_required
def admin(request):
	q = BugModel.objects.all()
	table = SimpleTable(q)
	RequestConfig(request).configure(table)
	return render(request, 'bugreports.html', {'table':table} )

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
		city = geocity.record_by_addr(ip)
		video_quality = request.GET.get('quality', None)
		video_format = request.GET.get('format', None)
		stream_title = request.GET.get('path', None)
		data = {'ip':ip, 
			'city': city['city'],
			'country': city['country_name'],
			'timezone': city['time_zone'],
			'video_format': video_format,
			'video_quality': video_quality,
			'stream_title': stream_title
		}
		
		form = BugForm(initial=data)
		
	return render(request, 'data.html', { 'form': form, })
	
def bug_search(request):
	if request.method == 'POST':
		desc = request.POST.get('desc')
		q = BugModel.objects.filter(desc__icontains=desc)
		table = SimpleTable(q)
		RequestConfig(request).configure(table)
		return render(request, 'bugreports.html', {'table':table} )
	else:
		form = SearchForm()
		return render(request, 'bug_search.html', {'form' : form} )
	#return HttpResponse('My mind palace')

def bug_edit(request, pk):
	if request.method == 'POST':
		record = BugModel.objects.get(pk=pk)
		form = EditForm(request.POST, instance=record)
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
		
		form = EditForm(initial=data)
	return render(request, 'editbugform.html', { 'form': form, })
	
def bug_delete(request, pk):
	record = BugModel.objects.get(pk=pk)
	record.delete()
	return HttpResponseRedirect('../../admin')
		
def logout_user(request):
	logout(request)
	return index(request)
