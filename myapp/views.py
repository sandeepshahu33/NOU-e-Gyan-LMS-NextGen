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
            elif user.groups.filter(name='Teacher').exists():
                login(req, user)
                messages.success(req, "Teacher logged in successfully!")
                return redirect('teacherdash')
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
        session_id=req.POST['session_id']
        level=req.POST['level']
        duration=req.POST['duration']
        description=req.POST['description']
        status=req.POST['status']
        selected_session=AcademicSession.objects.get(id=session_id)
        Course.objects.create(course_name=course_name,course_code=course_code,session_id=selected_session,level=level,duration=duration,description=description,status=status)
        messages.success(req,"Course is added successfully!!")
        return redirect('admindash')
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
        username_id=req.POST['username_id']
        # Actual user find krna  
        user_account=User.objects.get(id=username_id)
        password=req.POST['password']
        status=req.POST['status']
        Teacher.objects.create(employee_id=employee_id,name=name,email=email,mobile=mobile,department=department,designation=designation,username=user_account,password=password,status=status)
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

# Teacher view
def teacherdash(req):
    return render(req,"teacher/teacherdash.html")

