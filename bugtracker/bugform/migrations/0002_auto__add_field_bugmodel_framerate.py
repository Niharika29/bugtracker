# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BugModel.framerate'
        db.add_column(u'bugform_bugmodel', 'framerate',
                      self.gf('django.db.models.fields.FloatField')(default='0'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BugModel.framerate'
        db.delete_column(u'bugform_bugmodel', 'framerate')


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