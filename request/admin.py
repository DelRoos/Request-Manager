from django.contrib import admin
from .models import Template, RequestHistory, Comment, RequestImage

# admin.site.register(RequestHistory)
# admin.site.register(RequestImage)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("request_history", 'user', 'content', )



class TemplateAdmin(admin.ModelAdmin):
    list_display = ("objet", "student", 'publish_date', 'status', )

admin.site.register(Comment, CommentAdmin)
admin.site.register(Template, TemplateAdmin)
