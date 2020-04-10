from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    path('CourseData',views.CourseData, name='CourseData'),
]