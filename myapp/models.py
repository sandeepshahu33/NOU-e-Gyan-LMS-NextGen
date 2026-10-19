from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AcademicSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_name=models.CharField(max_length=30,unique=True)
    start_date=models.DateField()
    end_date=models.DateField()
    status=models.CharField(max_length=20)
    create_at=models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    session_id=models.ForeignKey(AcademicSession,on_delete=models.SET_NULL,null=True,related_name='course')
    course_name=models.CharField(max_length=150)
    course_code=models.CharField(max_length=30,unique=True)
    level=models.CharField(max_length=50)
    duration=models.CharField(max_length=50)
    description=models.TextField()
    status=models.CharField(max_length=20)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id=models.CharField(max_length=30,unique=True)
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=254,unique=True)
    mobile=models.CharField(max_length=15)
    department=models.CharField(max_length=120)
    designation=models.CharField(max_length=120)
    username=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Teacher')
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=20)