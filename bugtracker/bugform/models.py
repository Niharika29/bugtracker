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
	
	NEW = 'NEW'
	RESOLVED = 'RES'
	DISCARDED = 'DIS'
	PATCH_TO_REVIEW = 'PTR'
	ASSIGNED = 'ASS'
	STATUS_CHOICES = (
		(NEW, 'New'),
		(ASSIGNED, 'Assigned'),
		(DISCARDED, 'Discard'),
		(PATCH_TO_REVIEW, 'Patch under review'),
		(RESOLVED, 'Resolved'),
	)
	bugstatus = models.CharField(max_length=100, default=NEW, choices = STATUS_CHOICES)
	bugpriority = models.CharField(max_length=100, default='Normal')
	
class AdminModel(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=20)
# Create your models here.
