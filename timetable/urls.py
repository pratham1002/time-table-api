from django.contrib import admin
from django.urls import path, include
from . import views, authRouters

urlpatterns=[
    path('', authRouters.index, name='index'),
    path('signUp', authRouters.signUp, name='signUp'),
    path('login', authRouters.login, name='login'),
    path('logout', authRouters.logout, name='logout'),
    path('home', authRouters.home, name='home'),
    path('CourseData',views.CourseData, name='CourseData'),
    path('AddSlot',views.AddSlot, name='AddSlot'),
    path('RemoveCourse',views.RemoveCourse, name='RemoveCourse'),
    path('clear',views.clear,name='clear')
]