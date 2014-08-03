from django.db import models

class BugModel(models.Model):
	email = models.CharField(max_length=200)
	desc = models.CharField(max_length=500)
	date = models.DateField()
	loadtime = models.FloatField()
	os = models.CharField(max_length=200)
	browser = models.CharField(max_length=200)
	netspeed = models.FloatField()
	ip = models.CharField(max_length=40)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	timezone = models.CharField(max_length=100)
	framerate = models.FloatField(default='0')
	
	STATUS_CHOICES = (
		('New', 'New'),
		('Assigned', 'Assigned'),
		('Discard', 'Discard'),
		('Patch to review', 'Patch under review'),
		('Resolved', 'Resolved'),
	)
	bugstatus = models.CharField(max_length=100, default='New', choices = STATUS_CHOICES)
	
	PRIORITY_CHOICES = (
		('High', 'High'),
		('Normal','Normal'),
		('Low', 'Low'),
	)
	bugpriority = models.CharField(max_length=100, default='Normal', choices = PRIORITY_CHOICES)
	
class AdminModel(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=20)
# Create your models here.
