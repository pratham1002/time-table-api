from django.db import models
from  django.contrib.postgres.fields import ArrayField

# Create your models here.

class Student(models.Model):
    bits_id=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    name=models.CharField(max_length=100)

class Day(models.Model):
    day_number=models.IntegerField()
    student=models.ForeignKey(Student, on_delete=models.CASCADE)

class Hour(models.Model):
    day_number=models.IntegerField()
    hour_number=models.IntegerField()
    status=models.BooleanField(default=False)
    course=models.CharField(max_length=100)
    day=models.ForeignKey(Day, on_delete=models.CASCADE)
