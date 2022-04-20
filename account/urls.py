from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    # path('', views.index, name= 'index'),
    # path('login/', views.login_view, name='login_view'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('jurypage/', views.jury, name='jury'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),
]