from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	myname = 'Niharika';
	template = 'data.html'
	context = { 'some_name': myname }
	return render(request, template, context)
