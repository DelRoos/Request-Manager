from django.urls import path
from . import views

app_name = "request"

urlpatterns = [
    path('note/', views.NoteRequest, name='NoteRequest'),
    path('operation_requete/',views.operation_requete, name='operation_requete'),
    path('notification/',views.notification, name='notification'),
]