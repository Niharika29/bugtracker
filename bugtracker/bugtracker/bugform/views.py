from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.gis.utils import GeoIP
import pygeoip
from bugform.forms import BugForm

# Create your views here.
	
def index(request):
	if request.method == 'POST':
		form = BugForm(request.POST)
		if form.is_valid():
			form.save()
			#formInstance = form.save(commit=False)
			#formInstance.date = request.date
			#formInstance.email = request.email
			#formInstance.desc = request.desc
			#formInstance.save()
            #Process data in form.cleaned_data
			name = 'Niharika'
			template = 'postform.html'
			email = request.POST['email']
			bug = request.POST['desc']
			#image = request.POST['img']
			ip = getip(request)
			geocity = pygeoip.GeoIP('GeoLiteCity.dat')
			city = geocity.record_by_addr('122.161.236.2')
			context = { 'name':name, 'email':email, 'bug':bug, 'ip':ip, 'city':city['city'], 'country':city['country_name'], 'timezone':city['time_zone'] }
			return render(request, template, context)

	else:
		form = BugForm()
		
	return render(request, 'data.html', { 'form': form, })
	
def getip(request):
	xforwardedfor = request.META.get('HTTP_X_FORWARDED_FOR')
	if xforwardedfor:
		ip = xforwardedfor.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR') 
	return ip
