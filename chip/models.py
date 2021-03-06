# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
class Chip(models.Model):


	"""创建表结构"""
	title = models.CharField(max_length=255)
	summary = models.CharField(max_length=255, verbose_name='摘要')
	author = models.CharField(max_length=255, verbose_name='作者')
	pub_time = models.DateTimeField('原文发布时间')
	url  = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
	source = models.IntegerField(default=0)
	detail = models.TextField(default='')
	created_at = models.DateTimeField('抓取时间')
	updated_at = models.DateTimeField('datetime updated')
	author_url = models.CharField(max_length=255)

	class Meta: 
		db_table = u'chips'

	## hick 定义显示的列表: admin.py 中有类似 admin.site.register(Chip, ChipAdmin) 的定义则不走这里
	# def __str__(self):
	# 	return "%s  - %s " % (self.title, self.created_at)
