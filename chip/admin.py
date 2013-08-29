# -*- coding: UTF-8 -*-
from django.contrib import admin
from chip.models import Chip


# admin.site.register(Chip)

# 定制显示列表
class ChipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time', 'created_at', 'url')
admin.site.register(Chip, ChipAdmin)