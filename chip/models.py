# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
class Chip(models.Model):


	"""创建表结构"""
	title = models.CharField(max_length=255)
	summary = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	pub_time = models.DateTimeField('datetime published')
	url  = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
	source = models.IntegerField(default=0)
	detail = models.TextField(default='')
	created_at = models.DateTimeField('datetime created')
	updated_at = models.DateTimeField('datetime updated')
	author_url = models.CharField(max_length=255)

	class Meta: 
		db_table = u'chips'

	def __str__(self):
		return self.title