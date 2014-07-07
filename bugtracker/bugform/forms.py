from django.forms import ModelForm
from bugform.models import BugModel, AdminModel
import django_tables2 as tables

class BugForm(ModelForm):
	class Meta:
		model = BugModel
		fields = ['email', 'desc', 'date', 'loadtime', 'city', 'country', 'timezone', 'ip', 'netspeed', 'os', 'browser']
		
class AdminForm(ModelForm):
	class Meta:
		model = AdminModel
		fields = ['username', 'password']
		
class SimpleTable(tables.Table):
	class Meta:
		model = BugModel
		
#form = BugForm()
