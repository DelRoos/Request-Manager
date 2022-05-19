from django.urls import path
from . import views
from .views import delete_template

app_name = "request"

urlpatterns = [
    path('note/', views.NoteRequest, name='NoteRequest'),
    path('operation_requete/',views.operation_requete, name='operation_requete'),
    path('notification/<int:id>',views.notification, name='notification'),
    path('preview/<int:id>',views.preview, name='preview'),
    path('delete_template/<int:template_id>/', views.delete_template, name='delete-template'),
    path('edit', views.edit, name="edit"),
]