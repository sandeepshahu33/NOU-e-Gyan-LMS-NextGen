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
    session=models.CharField(max_length=150)
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
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Teacher')
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    course=models.CharField(max_length=150)
    subject_name=models.CharField(max_length=150)
    subject_code=models.CharField(max_length=30,unique=True)
    semester=models.CharField(max_length=50)
    credits=models.IntegerField()
    teacher=models.CharField(max_length=150)
    description=models.TextField()
    status=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.subject_name} -- {self.subject_code}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    enrollment_no=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=254,unique=True)
    mobile=models.CharField(max_length=15)
    course=models.CharField(max_length=150)
    session=models.CharField(max_length=150)
    semester=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Student')
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class StudyMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=180)
    course=models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    material_type=models.CharField(max_length=30)
    file=models.FileField(upload_to='study_material',null=True,blank=True)
    external_url=models.CharField(max_length=200,null=True)
    description=models.TextField()
    uploaded_by=models.CharField(max_length=150)
    status=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

