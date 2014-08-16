from django.forms import ModelForm
from bugform.models import BugModel, AdminModel
import django_tables2 as tables
from django_tables2.utils import A
from django import forms

class BugForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(BugForm, self).__init__(*args, **kwargs)
		self.fields['desc'].label = "Description"
		self.fields['bugpriority'].label = "Bug Priority"
	class Meta:
		model = BugModel
		fields = ['email', 'desc', 'date', 'loadtime', 'city', 'country', 'timezone', 'ip', 'netspeed', 'os', 'browser', 'bugstatus','bugpriority', 'video_format', 'video_quality', 'stream_title']
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
			'bugpriority':forms.RadioSelect(),
			'video_format':forms.HiddenInput(),
			'video_quality':forms.HiddenInput(),
			'stream_title': forms.HiddenInput()
		}

class SearchForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['desc'].label = "Description"
	class Meta:
		model = BugModel
		fields = ['desc']
		
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
