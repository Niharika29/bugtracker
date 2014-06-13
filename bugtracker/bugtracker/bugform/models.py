from django.db import models

class BugModel(models.Model):
	email = models.CharField(max_length=200)
	desc = models.CharField(max_length=500)
	date = models.DateField()
	loadtime = models.FloatField()
	
# Create your models here.
