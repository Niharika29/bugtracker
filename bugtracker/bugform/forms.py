from django.forms import ModelForm
from bugform.models import BugModel, AdminModel
import django_tables2 as tables
from django_tables2.utils import A
from django import forms

class BugForm(ModelForm):
	class Meta:
		model = BugModel
		fields = ['email', 'desc', 'date', 'loadtime', 'city', 'country', 'timezone', 'ip', 'netspeed', 'os', 'browser', 'bugstatus','bugpriority']
		widgets = {
			'browser':forms.HiddenInput(),
			'os':forms.HiddenInput(),
			'city':forms.HiddenInput(),
			'loadtime':forms.HiddenInput(),
			'date':forms.HiddenInput(),
			'country':forms.HiddenInput(),
			'bugstatus':forms.HiddenInput(),
			'timezone':forms.HiddenInput(),
			'ip':forms.HiddenInput(),
			'netspeed':forms.HiddenInput(),
			'desc':forms.Textarea,
			'bugpriority':forms.RadioSelect()
		}

		
class AdminForm(ModelForm):
	class Meta:
		model = AdminModel
		fields = ['username', 'password']
		
class SimpleTable(tables.Table):
	edit_link = tables.LinkColumn('bugform.views.bug_edit', args=[A('pk')], verbose_name='Edit', accessor='pk', attrs={'class':'edit_link'})
	delete_link = tables.LinkColumn('bugform.views.bug_delete', args=[A('pk')], verbose_name='Delete Bug', accessor='pk', attrs={'class':'delete_link'})
	class Meta:
		attrs = {'class' : 'paleblue'}
		model = BugModel
