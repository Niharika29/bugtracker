from django.conf.urls import patterns, url

from bugform import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'admin', views.admin, name='admin'),
	url(r'admin/edit/(?P<pk>\d+)/', views.bug_edit, name='bug_edit'),
	url(r'admin/delete/(?P<pk>\d+)/', views.bug_delete, name='bug_delete'),
	#url(r'admin/bugreports', views.)
)
