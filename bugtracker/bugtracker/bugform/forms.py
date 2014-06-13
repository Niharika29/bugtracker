from django.forms import ModelForm
from bugform.models import BugModel

class BugForm(ModelForm):
	class Meta:
		model = BugModel
		fields = ['email', 'desc', 'date', 'loadtime']
		
#form = BugForm()
