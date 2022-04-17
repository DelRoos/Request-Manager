from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('jurypage/', views.jury, name='jurypage'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),
]