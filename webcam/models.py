from django.db import models
from django.conf import settings


# Create your models here.
class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name_class = models.CharField(max_length=50)
    value = models.CharField(max_length=2)
    def __str__(self):
        return str(self.id)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=50, null= False)
    mssv  = models.CharField(max_length=8, null= False)
    Class = models.ForeignKey(Class, on_delete = models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)

class Authentication(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date  = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)