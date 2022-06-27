from django.urls import path
from . import views
from .views import delete_template

app_name = "request"

urlpatterns = [
    path('note/', views.NoteRequest, name='NoteRequest'),
    path('operation_requete/',views.operation_requete, name='operation_requete'),
    path('operation_edit_requete/<int:id>/',views.operation_edit_requete, name='operation_edit_requete'),
    path('notification/<int:id>/',views.notification, name='notification'),
    path('preview/<int:id>/',views.preview, name='preview'),
    path('follow/<int:id>/',views.follow, name='follow'),
    path('delete_template/<int:template_id>/', views.delete_template, name='delete-template'),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('post_comment/', views.post_comment, name="post_comment"),
    path('change_state/', views.change_state, name="change_state"),
    path('transfert_request/', views.transfert_request, name="transfert_request"),
    
    path('request_asset/', views.file_upload),
]
