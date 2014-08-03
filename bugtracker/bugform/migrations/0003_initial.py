# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BugModel'
        db.create_table(u'bugform_bugmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('loadtime', self.gf('django.db.models.fields.FloatField')()),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('netspeed', self.gf('django.db.models.fields.FloatField')()),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('bugstatus', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('bugpriority', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('framerate', self.gf('django.db.models.fields.FloatField')(default='0')),
        ))
        db.send_create_signal(u'bugform', ['BugModel'])

        # Adding model 'AdminModel'
        db.create_table(u'bugform_adminmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'bugform', ['AdminModel'])


    def backwards(self, orm):
        # Deleting model 'BugModel'
        db.delete_table(u'bugform_bugmodel')

        # Deleting model 'AdminModel'
        db.delete_table(u'bugform_adminmodel')


    models = {
        u'bugform.adminmodel': {
            'Meta': {'object_name': 'AdminModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'bugform.bugmodel': {
            'Meta': {'object_name': 'BugModel'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bugpriority': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bugstatus': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'framerate': ('django.db.models.fields.FloatField', [], {'default': "'0'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'loadtime': ('django.db.models.fields.FloatField', [], {}),
            'netspeed': ('django.db.models.fields.FloatField', [], {}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bugform']