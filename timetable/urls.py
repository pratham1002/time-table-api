from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('signUp',views.signUp,name='signUp'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('home',views.home, name='home'),
    path('CourseData',views.CourseData, name='CourseData'),
    path('AddSlot',views.AddSlot, name='AddSlot'),
    path('RemoveCourse',views.RemoveCourse, name='RemoveCourse'),
    path('clear',views.clear,name='clear')
]