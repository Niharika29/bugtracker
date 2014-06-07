from django.conf.urls import patterns, url

from bugform import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^formprocess$', views.formprocess, name='formprocess')
)
