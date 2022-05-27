from django.contrib import admin
from .models import Template, RequestHistory, Comment

admin.site.register(Template)
admin.site.register(RequestHistory)
admin.site.register(Comment)