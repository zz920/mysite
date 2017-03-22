from django.contrib import admin
from .models import *

class WebPageInfo(admin.ModelAdmin):
    list_display = ('title', 'date',)

admin.site.register(WebPage, WebPageInfo)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(UserInfo)
