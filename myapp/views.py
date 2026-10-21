from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(req):
    if req.method== "POST":
        username=req.POST['username']
        password=req.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(req,user)
                messages.success(req,"User Loggedin successfully!!")
                return redirect('admindash')
            elif hasattr(user,'Teacher'):
                login(req, user)
                messages.success(req, "Teacher logged in successfully!")
                return redirect('teacherdash')
            elif hasattr(user,'Student'):
                active_student=Student.objects.filter( user=user,status="Active").exists()
                if active_student:
                    login(req, user)
                    messages.success(req, "Student logged in successfully!")
                    return redirect('studentdash')
                else:
                    messages.error(req,"Your account is blocked. Contact to our team !!")
                    return redirect('index')
        else:
            messages.error(req,"you have entered wrong email or password !!")
            return redirect('index')
    return render(req,'index.html')


@login_required
def admindash(req):
    return render(req,'admin/admindash.html')

@login_required
def add_session(req):
    sessions=AcademicSession.objects.all()
    if req.method == 'POST':
        session_name=req.POST['session_name']
        start_date=req.POST['start_date']
        end_date=req.POST['end_date']
        status=req.POST['status']
        session_exist=AcademicSession.objects.filter(session_name=session_name).exists()
        if session_exist:
            messages.error(req,'Session is already exits !!')
            return redirect('admindash')
        elif start_date > end_date:
            messages.error(req,"You enterd wrong session !! ")
            return redirect('add_session')
        else:
            AcademicSession.objects.create(session_name=session_name,start_date=start_date,end_date=end_date,status=status)
            messages.success(req,"Session added successfully!!")
    return render(req,'admin/add_session.html',{"sessions":sessions})

def view_sessions(req):
    sessions=AcademicSession.objects.all()
    active_count=AcademicSession.objects.filter(status="Active").count()
    upcoming_count=AcademicSession.objects.filter(status="Upcoming").count()
    return render(req,"admin/view_sessions.html",{"sessions":sessions,"active_count":active_count,"upcoming_count":upcoming_count})

@login_required
def edit_session(req,id):
    session=AcademicSession.objects.get(id=id)
    if req.method == "POST":
        session.session_name=req.POST['session_name']
        session.start_date=req.POST['start_date']
        session.end_date=req.POST['end_date']
        session.status=req.POST['status']
        session.save()
        messages.success(req,"Session updated successfully!!")
        return redirect('view_sessions')
    return render(req,"admin/edit_session.html",{"session":session})

@login_required
def delete_session(req,id):
    session=AcademicSession.objects.get(id=id)
    if req.method == "POST":
        session.delete()
        messages.success(req,"Session deleted successfully!!")
        return redirect('view_sessions')
    return render(req,"admin/delete_session.html",{"session":session})

@login_required
def add_course(req):
    session=AcademicSession.objects.filter(status="Active").all()
    if req.method == "POST":
        course_name=req.POST['course_name']
        course_code=req.POST['course_code']
        session=req.POST['session']
        level=req.POST['level']
        duration=req.POST['duration']
        description=req.POST['description']
        status=req.POST['status']
        Course.objects.create(course_name=course_name,course_code=course_code,session=session,level=level,duration=duration,description=description,status=status)
        messages.success(req,"Course is added successfully!!")
        return redirect('view-courses')
    return render(req,'admin/add_course.html',{"sessions":session})

def view_courses(req):
    courses=Course.objects.all()
    active_count=Course.objects.filter(status="Active").count()
    inactive_count=Course.objects.filter(status="Inactive").count()

    context={
        'courses':courses,
        "active_count":active_count,
        "inactive_count":inactive_count
    }
    return render(req,"admin/view_courses.html",context)

def edit_course(req,id):
    sessions=AcademicSession.objects.filter(status="Active").all()
    course=Course.objects.get(id=id)
    context={
        "course":course,
        'sessions':sessions,
    }
    if req.method=="POST":
        course_name=req.POST['course_name']
        course_code=req.POST['course_code']
        session_id=req.POST['session_id']
        level=req.POST['level']
        duration=req.POST['duration']
        description=req.POST['description']
        status=req.POST['status']
        selected_session=AcademicSession.objects.get(id=session_id)
        Course.objects.filter(id=id).update(course_name=course_name,course_code=course_code,session_id=selected_session,level=level,duration=duration,description=description,status=status)
        print(session_id)
        messages.success(req,"Course updated successfully !!")
        return redirect('view_courses')
    return render(req,"admin/edit_course.html",context)

def delete_course(req,id):
    course=Course.objects.get(id=id)
    if req.method == 'POST':
        course.delete()
        messages.success(req,"Course deleted successfully !! ")
        return redirect('view_courses')
    return render(req,"admin/delete_course.html",{'course':course})

@login_required
def user_logout(req):
    logout(req)
    messages.success(req,"You logged out successfully !! ")
    return redirect('index')

def add_teacher(req):
    users=User.objects.all()
    if req.method == 'POST':
        employee_id=req.POST['employee_id']
        name=req.POST['name']
        email=req.POST['email']
        mobile=req.POST['mobile']
        department=req.POST['department']
        designation=req.POST['designation']
        user=req.POST['username']
        password=req.POST['password']
        status=req.POST['status']
        user_obj=User.objects.create_user(username=user,password=password,email=email)
        Teacher.objects.create(employee_id=employee_id,name=name,email=email,mobile=mobile,department=department,designation=designation,user=user_obj,password=password,status=status)
        messages.success(req,"Teacher added successfully !!")
        return redirect('add_teacher')
    return render(req,"admin/add_teacher.html",{"users":users})

def view_teacher(req):
    teachers=Teacher.objects.all()
    active_count=Teacher.objects.filter(status="Active").count()
    department_count=Teacher.objects.values_list('department',flat=True).distinct().count()
    context={
        'teachers':teachers,
        'active_count':active_count,
        'department_count':department_count
    }
    return render(req,'admin/view_teacher.html',context)

def add_subject(req):
    teachers=Teacher.objects.all()
    if req.method == "POST":
        course=req.POST['course']
        subject_name=req.POST['subject_name']
        subject_code=req.POST['subject_code']
        semester=req.POST['semester']
        credits=req.POST['credits']
        teacher=req.POST['teacher']
        description=req.POST['description']
        status=req.POST['status']
        Subject.objects.create(course=course,subject_name=subject_name,subject_code=subject_code,semester=semester,credits=credits,teacher=teacher,description=description,status=status)
        messages.success(req,"Subject added successfullly !! ")
        return redirect('view_subjects')
    return render(req,"admin/add_subject.html",{"teachers":teachers})

def view_subjects(req):
    subjects=Subject.objects.all()
    active_count=Subject.objects.filter(status="Active").count()
    inactive_count=Subject.objects.filter(status="Inactive").count()
    semesters=Subject.objects.values_list("semester",flat=True)
    context={
        "subjects":subjects,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "semesters":semesters
    }
    return render(req,"admin/view_subjects.html",context)

def add_student(req):
    if req.method == "POST":
        enrollment_no=req.POST['enrollment_no']
        name=req.POST['name']
        email=req.POST['email']
        mobile=req.POST['mobile']
        course=req.POST['course']
        session=req.POST['session']
        semester=req.POST['semester']
        user=req.POST['username']
        password=req.POST['password']
        status=req.POST['status']
        user_obj=User.objects.create_user(username=user,password=password,email=email)
        Student.objects.create(enrollment_no=enrollment_no,name=name,email=email,mobile=mobile,course=course,session=session,semester=semester,user=user_obj,password=password,status=status)
        messages.success(req,"Student added successfully !! ")
        return redirect('view_students')
    return render(req,"admin/add_student.html")

def view_students(req):
    students=Student.objects.all()
    active_count=Student.objects.filter(status="Active").count()
    inactive_count=Student.objects.filter(status="Inactive").count()
    semesters=Student.objects.values_list("semester",flat=True)
    courses=Student.objects.values_list("course",flat=True)
    context={
        "students":students,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "semesters":semesters,
        "courses":courses
    }
    return render(req,"admin/view_students.html",context)

def add_studymaterial(req):
    teachers=Teacher.objects.filter(status="Active").all()
    return render(req,"admin/add_studymaterial.html",{"teachers":teachers})

def view_studymaterial(req):
    return render(req,"admin/view_studymaterial.html")
# Teacher view
def teacherdash(req):
    return render(req,"teacher/teacherdash.html")
# Student view
def studentdash(req):
    return render(req,"student/studentdash.html")

