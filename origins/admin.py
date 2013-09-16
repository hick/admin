# -*- coding: UTF-8 -*-
from django.contrib import admin
from origins.models import Origins


# 定制显示列表
class OriginsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'last_time', 'next_time', 'item_time', 'url', 'msg', 'day_count', 'rev1', 'rev2', 'desc')
admin.site.register(Origins, OriginsAdmin)