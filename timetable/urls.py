from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('SignUp',views.SignUp,name='SignUp'),
    path('Login',views.Login,name='Login'),
    path('NewUser',views.CreateUser,name='CreateUser'),
    path('FindUser',views.LoginUser,name='LoginUser'),
    path('Logout',views.Logout,name='Logout'),
    path('Home',views.Home, name='home'),
    path('CourseData',views.CourseData, name='CourseData'),
    path('AddSlot',views.AddSlot, name='AddSlot'),
    path('RemoveCourse',views.RemoveCourse, name='RemoveCourse'),
    path('clear',views.clear,name='clear')
]