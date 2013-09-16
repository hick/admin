# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
class Origins(models.Model):


    """创建表结构"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    # type = models.CharField(max_length=255)
    msg = models.CharField(max_length=255)
    day_count = models.IntegerField(default=8)
    rev1 = models.CharField(max_length=255)
    rev2 = models.CharField(max_length=255)
    last_time = models.DateTimeField('最后时间')
    next_time = models.DateTimeField('下次时间')
    item_time = models.DateTimeField('数据时间')
    desc = models.TextField(default='')

    # summary = models.CharField(max_length=255, verbose_name='摘要')
    # author = models.CharField(max_length=255, verbose_name='作者')
    # pub_time = models.DateTimeField('原文发布时间')
    # url  = models.CharField(max_length=255)
    # tags = models.CharField(max_length=255)
    # source = models.IntegerField(default=0)
    # detail = models.TextField(default='')
    # created_at = models.DateTimeField('抓取时间')
    # updated_at = models.DateTimeField('datetime updated')
    # author_url = models.CharField(max_length=255)

    class Meta: 
        db_table = u'origins'