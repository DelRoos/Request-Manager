from django.contrib import admin
from .models import Template, RequestHistory, Comment, RequestImage

admin.site.register(Template)
admin.site.register(RequestHistory)
admin.site.register(Comment)
admin.site.register(RequestImage)