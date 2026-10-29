from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date
from django.utils import timezone
# Create your views here.

from django.contrib.auth.decorators import login_required
import csv
import json
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.apps import apps
from django.utils import timezone
from django.db import transaction
from django.urls import reverse
from urllib.parse import quote
from pprint import pprint

# Google Meet integration lives in google_meet.py; keep URL-facing names here.
from .google_meet import (
    google_login, google_callback, schedule_meeting, start_meeting,
    student_classes, join_meeting, teacher_meetings, superadmin_meetings,
)
from .models import GoogleMeeting

from .compiler_helper import LANGUAGES, STARTER_CODE, run_code
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from .compiler_helper import LANGUAGES, STARTER_CODE, run_code



def index(req):
    if req.method== "POST":
        username=req.POST['username']
        password=req.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(req,user)
                messages.success(req,"Super Admin Loggedin successfully!!")
                return redirect('admindash')
            elif hasattr(user,'Teacher'):
                active_teacher=tbl_teacher.objects.filter( user=user,status="Active").exists()
                if active_teacher:
                    login(req, user)
                    messages.success(req, "Teacher logged in successfully!")
                    return redirect('teacherdash')
                else:
                    messages.error(req,"Your account is blocked. Contact to our team !!")
                    return redirect('index')
            elif hasattr(user,'Student'):
                active_student=tbl_student.objects.filter( user=user,status="Active").exists()
                if active_student:
                    login(req, user)
                    messages.success(req, "tbl_student logged in successfully!")
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

    # TOTAL COUNTS

    total_students = tbl_student.objects.count()
    total_teachers = tbl_teacher.objects.count()
    total_courses = tbl_course.objects.count()
    total_subjects = tbl_subject.objects.count()
    total_materials = StudyMaterial.objects.count()
    total_assignments = Assignment.objects.count()
    total_sessions = AcademicSession.objects.count()

    # ACTIVE COUNTS

    active_students = tbl_student.objects.filter(
        status__iexact='Active'
    ).count()

    active_teachers = tbl_teacher.objects.filter(
        status__iexact='Active'
    ).count()

    active_courses = tbl_course.objects.filter(
        status__iexact='Active'
    ).count()

    active_materials = StudyMaterial.objects.filter(
        status__iexact='Active'
    ).count()

    # STUDENT ANALYSIS

    students_by_course = (
        tbl_student.objects
        .values('course')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    students_by_session = (
        tbl_student.objects
        .values('session')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # COURSE ANALYSIS

    courses_by_level = (
        tbl_course.objects
        .values('level')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # MATERIAL ANALYSIS

    materials_by_type = (
        StudyMaterial.objects
        .values('material_type')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # ASSIGNMENT ANALYSIS

    assignments_by_course = (
        Assignment.objects
        .values('course')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # RECENT STUDENTS

    recent_students = tbl_student.objects.order_by('-id')[:5]

    # RECENT MATERIALS

    recent_materials = StudyMaterial.objects.order_by(
        '-created_at'
    )[:5]

    # RECENT ASSIGNMENTS

    recent_assignments = Assignment.objects.order_by(
        '-created_at'
    )[:5]

    # RECENT SESSIONS

    recent_sessions = AcademicSession.objects.order_by(
        '-create_at'
    )[:5]

    # CURRENT ACADEMIC SESSION

    current_session = AcademicSession.objects.filter(
        start_date__lte=date.today(),
        end_date__gte=date.today()
    ).first()

    # UPCOMING ASSIGNMENTS

    upcoming_assignments = Assignment.objects.filter(
        due_date__gte=date.today()
    ).order_by('due_date')[:5]

    # CONTEXT

    context = {
        # Main KPI
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_subjects': total_subjects,
        'total_materials': total_materials,
        'total_assignments': total_assignments,
        'total_sessions': total_sessions,

        # Active
        'active_students': active_students,
        'active_teachers': active_teachers,
        'active_courses': active_courses,
        'active_materials': active_materials,

        # Analysis
        'students_by_course': students_by_course,
        'students_by_session': students_by_session,
        'courses_by_level': courses_by_level,
        'materials_by_type': materials_by_type,
        'assignments_by_course': assignments_by_course,

        # Recent
        'recent_students': recent_students,
        'recent_materials': recent_materials,
        'recent_assignments': recent_assignments,
        'recent_sessions': recent_sessions,

        # Other
        'current_session': current_session,
        'upcoming_assignments': upcoming_assignments,
    }
    return render(req,'admin/admindash.html',context)

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
            return redirect('view_sessions')
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
        tbl_course.objects.create(course_name=course_name,course_code=course_code,session=session,level=level,duration=duration,description=description,status=status)
        messages.success(req,"Course is added successfully!!")
        return redirect('view_courses')
    return render(req,'admin/add_course.html',{"sessions":session})

def view_courses(req):
    courses=tbl_course.objects.all()
    active_count=tbl_course.objects.filter(status="Active").count()
    inactive_count=tbl_course.objects.filter(status="Inactive").count()

    context={
        'courses':courses,
        "active_count":active_count,
        "inactive_count":inactive_count
    }
    return render(req,"admin/view_courses.html",context)

def edit_course(req,id):
    sessions=AcademicSession.objects.filter(status="Active").all()
    course=tbl_course.objects.get(id=id)
    context={
        "course":course,
        'sessions':sessions,
    }
    if req.method=="POST":
        course_name=req.POST['course_name']
        course_code=req.POST['course_code']
        session=req.POST['session']
        level=req.POST['level']
        duration=req.POST['duration']
        description=req.POST['description']
        status=req.POST['status']
        tbl_course.objects.filter(id=id).update(course_name=course_name,course_code=course_code,session=session,level=level,duration=duration,description=description,status=status)
        messages.success(req,"Course updated successfully !!")
        return redirect('view_courses')
    return render(req,"admin/edit_course.html",context)

def delete_course(req,id):
    course=tbl_course.objects.get(id=id)
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
        tbl_teacher.objects.create(employee_id=employee_id,name=name,email=email,mobile=mobile,department=department,designation=designation,user=user_obj,password=password,status=status)
        messages.success(req,"Teacher added successfully !!")
        return redirect('view_teacher')
    return render(req,"admin/add_teacher.html",{"users":users})

def view_teacher(req):
    teachers=tbl_teacher.objects.all()
    active_count=tbl_teacher.objects.filter(status="Active").count()
    department_count=tbl_teacher.objects.values_list('department',flat=True).distinct().count()
    context={
        'teachers':teachers,
        'active_count':active_count,
        'department_count':department_count
    }
    return render(req,'admin/view_teacher.html',context)

def edit_teacher(req,id):
    teacher=tbl_teacher.objects.get(id=id)
    if req.method == 'POST':
        employee_id=req.POST['employee_id']
        name=req.POST['name']
        email=req.POST['email']
        mobile=req.POST['mobile']
        department=req.POST['department']
        designation=req.POST['designation']
        password=req.POST['password']
        status=req.POST['status']

        teacher.employee_id=employee_id
        teacher.name=name
        teacher.email=email
        teacher.mobile=mobile
        teacher.department=department
        teacher.designation=designation
        teacher.status=status
        if password:
            teacher.password = password
            teacher.user.set_password(password)

        teacher.user.email = email
        teacher.user.save()
        teacher.save()
        messages.success(req,"Teacher updated successfully !!")
        return redirect('view_teacher')
    return render(req,"admin/edit_teacher.html",{"teacher":teacher})

def delete_teacher(req,id):
    teacher=tbl_teacher.objects.get(id=id)
    if req.method == "POST":
        teacher.user.delete()
        messages.success(req,"Teacher deleted successfully!!")
        return redirect('view_teacher')
    return render(req,"admin/delete_teacher.html",{"teacher":teacher})

def bulk_upload_teacher(req):
    if req.method=='POST':
        file=req.FILES.get("file")
        try:
            if file:
                data=file.read().decode('utf-8-sig').splitlines()
                header=csv.DictReader(data)
                for row in header:
                    user_obj=User.objects.create_user(username=row['username'],password=row['password'],email=row['email'])
                    tbl_teacher.objects.create(employee_id=row['employee_id'],name=row['name'],email=row['email'],mobile=row['mobile'],department=row['department'],designation=row['designation'],user=user_obj,password=row['password'],status=row['status'])
                messages.success(req,"Bulk Teacher uploaded successfullly !!")
                return redirect('view_teacher')
        except Exception as ex:
            print("Error : ",ex)
    return render(req,"admin/bulk_upload_teacher.html")

def add_subject(req):
    teachers=tbl_teacher.objects.all()
    courses=tbl_course.objects.filter(status="Active")
    if req.method == "POST":
        course=req.POST['course']
        subject_name=req.POST['subject_name']
        subject_code=req.POST['subject_code']
        semester=req.POST['semester']
        credits=req.POST['credits']
        teacher=req.POST['teacher']
        description=req.POST['description']
        status=req.POST['status']
        tbl_subject.objects.create(course=course,subject_name=subject_name,subject_code=subject_code,semester=semester,credits=credits,teacher=teacher,description=description,status=status)
        messages.success(req,"Subject added successfullly !! ")
        return redirect('view_subjects')
    context={
        "teachers":teachers,
        "courses":courses,
    }
    return render(req,"admin/add_subject.html",context)

def view_subjects(req):
    subjects=tbl_subject.objects.all()
    active_count=tbl_subject.objects.filter(status="Active").count()
    inactive_count=tbl_subject.objects.filter(status="Inactive").count()
    semesters=tbl_subject.objects.values_list("semester",flat=True).distinct()
    context={
        "subjects":subjects,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "semesters":semesters
    }
    return render(req,"admin/view_subjects.html",context)

def edit_subject(req,id):
    subject=tbl_subject.objects.get(id=id)
    teachers=tbl_teacher.objects.filter(status="Active")
    courses=tbl_course.objects.filter(status="Active")

    context={
        "subject":subject,
        "teachers":teachers,
        "courses":courses
    }
    if req.method == "POST":
        course=req.POST['course']
        subject_name=req.POST['subject_name']
        subject_code=req.POST['subject_code']
        semester=req.POST['semester']
        credits=req.POST['credits']
        teacher=req.POST['teacher']
        description=req.POST['description']
        status=req.POST['status']
        subject.course=course
        subject.subject_name=subject_name
        subject.subject_code=subject_code
        subject.semester=semester
        subject.credits=credits
        subject.teacher=teacher
        subject.description=description
        subject.status=status
        subject.save()
        messages.success(req,"Subject updated successfullly !! ")
        return redirect('view_subjects')
    return render(req,"admin/edit_subject.html",context)

def delete_subject(req,id):
    subject=tbl_subject.objects.get(id=id)
    context={
        "subject":subject,
    }
    if req.method == "POST":
        subject.delete()
        messages.success(req,"Subject deleted successfully !!")
        return redirect('view_subjects')
    return render(req,"admin/delete_subject.html",context)

def add_student(req):
    sessions=AcademicSession.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active")
    context={
        "sessions":sessions,
        "courses":courses,
    }
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
        tbl_student.objects.create(enrollment_no=enrollment_no,name=name,email=email,mobile=mobile,course=course,session=session,semester=semester,user=user_obj,password=password,status=status)
        messages.success(req,"tbl_student added successfully !! ")
        return redirect('view_students')
    return render(req,"admin/add_student.html",context)

def view_students(req):
    students=tbl_student.objects.all()
    active_count=tbl_student.objects.filter(status="Active").count()
    inactive_count=tbl_student.objects.filter(status="Inactive").count()
    semesters=tbl_student.objects.values_list("semester",flat=True).distinct()
    courses=tbl_student.objects.values_list("course",flat=True).distinct()
    context={
        "students":students,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "semesters":semesters,
        "courses":courses
    }
    return render(req,"admin/view_students.html",context)

def edit_student(req,id):
    student=tbl_student.objects.get(id=id)
    sessions=AcademicSession.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active")
    context={
        "sessions":sessions,
        "courses":courses,
        "student":student,
    }
    if req.method == "POST":
        enrollment_no=req.POST['enrollment_no']
        name=req.POST['name']
        email=req.POST['email']
        mobile=req.POST['mobile']
        course=req.POST['course']
        session=req.POST['session']
        semester=req.POST['semester']
        password=req.POST['password']
        status=req.POST['status']
        student.enrollment_no = enrollment_no
        student.name = name
        student.email = email
        student.mobile = mobile
        student.course = course
        student.session = session
        student.semester = semester
        student.status = status
        # Password only change when new password is entered
        if password:
            student.password = password
            student.user.set_password(password)
        # Email update in Django User
        student.user.email = email
        student.user.save()
        student.save()
        messages.success(req,"tbl_student data updated successfully !! ")
        return redirect('view_students')
    return render(req,"admin/edit_student.html",context)

def delete_student(req,id):
    student=tbl_student.objects.get(id=id)
    if req.method == "POST":
        student.user.delete()
        messages.success(req,"tbl_student deleted successfully!!")
        return redirect("view_students")
    return render(req,"admin/delete_student.html",{"student":student})

def bulk_upload_student(req):
    if req.method=='POST':
        file=req.FILES.get("file")
        try:
            if file:
                data=file.read().decode('utf-8-sig').splitlines()
                header=csv.DictReader(data)
                for row in header:
                    user_obj=User.objects.create_user(username=row['username'],password=row['password'],email=row['email'])
                    tbl_student.objects.create(enrollment_no=row['enrollment_no'],name=row['name'],email=row['email'],mobile=row['mobile'],course=row['course'],session=row['session'],semester=row['semester'],user=user_obj,password=row['password'],status=row['status'])
                messages.success(req,"Bulk students uploaded successfully !! ")
                return redirect('view_students')
        except Exception as ex:
            print("Error : ",ex)
    return render(req,"admin/bulk_upload_student.html")


def add_studymaterial(req):
    teachers=tbl_teacher.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active").all()
    subjects=tbl_subject.objects.filter(status="Active").all()
    context={
        "teachers":teachers,
        "courses":courses,
        "subjects":subjects,
    }
    if req.method == 'POST':
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        material_type=req.POST['material_type']
        file=req.FILES.get('file')
        external_url=req.POST['external_url']
        description=req.POST['description']
        uploaded_by=req.POST['uploaded_by']
        status=req.POST['status']
        StudyMaterial.objects.create(title=title,course=course,subject=subject,material_type=material_type,file=file,external_url=external_url,description=description,uploaded_by=uploaded_by,status=status)
        messages.success(req,"Study Material uploaded successfully!!")
        return redirect('view_studymaterial')
    return render(req,"admin/add_studymaterial.html",context)

def view_studymaterial(req):
    materials=StudyMaterial.objects.all()
    active_count=StudyMaterial.objects.filter(status="Active").count()
    inactive_count=StudyMaterial.objects.filter(status="Inactive").count()
    courses=tbl_course.objects.values_list('course_name',flat=True).distinct()
    material_types=StudyMaterial.objects.values_list('material_type',flat=True).distinct()
    context={
        "materials":materials,
        "active_count":active_count,
        "inactive_count":inactive_count,
        'courses':courses,
        'material_types':material_types,
        }
    return render(req,"admin/view_studymaterial.html",context)
def edit_studymaterial(req,id):
    material=StudyMaterial.objects.get(id=id)
    teachers=tbl_teacher.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active").all()
    subjects=tbl_subject.objects.filter(status="Active").all()
    context={
        "material":material,
        "teachers":teachers,
        "courses":courses,
        "subjects":subjects,
    }
    if req.method=="POST":
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        material_type=req.POST['material_type']
        file=req.FILES.get('file')
        external_url = req.POST.get('external_url', '').strip()
        description=req.POST['description']
        uploaded_by=req.POST['uploaded_by']
        status=req.POST['status']
        material.title=title
        material.course=course
        material.subject=subject
        material.material_type=material_type
        material.description=description
        material.uploaded_by=uploaded_by
        material.status=status
        if file:
            material.file=file
        if external_url:
            material.external_url=external_url
        material.save()
        messages.success(req,"Study material updated successfully !!")
        return redirect("view_studymaterial")
    return render(req,"admin/edit_studymaterial.html",context)

def delete_studymaterial(req,id):
    material=StudyMaterial.objects.get(id=id)
    if req.method == "POST":
        material.delete()
        messages.success(req,"Study material deleted successfully!!")
        return redirect("view_studymaterial")
    return render(req,"admin/delete_studymaterial.html",{"material":material})

def upload_assignment(req):
    teachers=tbl_teacher.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active").all()
    subjects=tbl_subject.objects.filter(status="Active").all()
    context={
        "teachers":teachers,
        "courses":courses,
        "subjects":subjects,
        }
    if req.method == 'POST':
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        due_date=req.POST['due_date']
        total_marks=req.POST['total_marks']
        attachment=req.FILES.get('attachment')
        instructions=req.POST['instructions']
        created_by=req.POST['created_by']
        status=req.POST['status']
        Assignment.objects.create(title=title,course=course,subject=subject,due_date=due_date,total_marks=total_marks,attachment=attachment,instructions=instructions,created_by=created_by,status=status)
        messages.success(req,"Assignment uploaded successfully!!")
        return redirect('view_assignment')
    return render(req,"admin/upload_assignment.html",context)

def view_assignment(req):
    assignments=Assignment.objects.all()
    active_count=Assignment.objects.filter(status="Active").count()
    inactive_count=Assignment.objects.filter(status="Inactive").count()
    courses=tbl_course.objects.values_list('course_name',flat=True).distinct()
    subjects=tbl_subject.objects.values_list('subject_name',flat=True).distinct()
    context={
        "assignments":assignments,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "courses":courses,
        "subjects":subjects,
    }
    return render(req,"admin/view_assignment.html",context)

def edit_assignment(req,id):
    assignment=Assignment.objects.get(id=id)
    teachers=tbl_teacher.objects.filter(status="Active").all()
    courses=tbl_course.objects.filter(status="Active").all()
    subjects=tbl_subject.objects.filter(status="Active").all()
    context={
        "assignment":assignment,
        "teachers":teachers,
        "courses":courses,
        "subjects":subjects,
    }
    if req.method == 'POST':
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        due_date=req.POST['due_date']
        total_marks=req.POST['total_marks']
        attachment=req.FILES.get('attachment')
        instructions=req.POST['instructions']
        created_by=req.POST['created_by']
        status=req.POST['status']
        assignment.title=title
        assignment.course=course
        assignment.subject=subject
        assignment.due_date=due_date
        assignment.total_marks=total_marks
        assignment.instructions=instructions
        assignment.created_by=created_by
        assignment.status=status
        if attachment:
            assignment.attachment=attachment
        assignment.save()
        messages.success(req,"Assignment updated successfully !! ")
        return redirect('view_assignment')
    return render(req,"admin/edit_assignment.html",context)

def delete_assignment(req,id):
    assignment=Assignment.objects.get(id=id)
    context={
        "assignment":assignment,
    }
    
    if req.method == "POST":
        assignment.delete()
        file_field=assignment.attachment
        if file_field:
            file_field.delete(save=False)
        messages.success(req,"Assignment deleted successfully !! ")
        return redirect('view_assignment')
    return render(req,"admin/delete_assignment.html",context)

# Teacher view
def teacherdash(req):
    username=tbl_teacher.objects.get(user=req.user)
    return render(req,"teacher/teacherdash.html",{"username":username})

def teacher_studymaterial(req):
    username=tbl_teacher.objects.get(user=req.user)
    courses=tbl_course.objects.filter(status="Active").all()
    subjects=tbl_subject.objects.filter(status="Active").all()
    context={
        "username":username,
        "courses":courses,
        "subjects":subjects,
    }
    if req.method == 'POST':
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        material_type=req.POST['material_type']
        file=req.FILES.get('file')
        external_url=req.POST['external_url']
        description=req.POST['description']
        uploaded_by=username.name
        status=req.POST['status']
        StudyMaterial.objects.create(title=title,course=course,subject=subject,material_type=material_type,file=file,external_url=external_url,description=description,uploaded_by=uploaded_by,status=status)
        messages.success(req,"Study Material uploaded successfully!!")
        return redirect('tchview_studymaterial')
    return render(req,"teacher/teacher_studymaterial.html",context)

def tchview_studymaterial(req):
    study_materials=StudyMaterial.objects.all()
    return render(req,"teacher/tchview_studymaterial.html",{"study_materials":study_materials})

def techupload_assignment(req):
    username=tbl_teacher.objects.get(user=req.user)
    if req.method == 'POST':
        title=req.POST['title']
        course=req.POST['course']
        subject=req.POST['subject']
        due_date=req.POST['due_date']
        total_marks=req.POST['total_marks']
        attachment=req.FILES.get('attachment')
        instructions=req.POST['instructions']
        created_by=username.name
        status=req.POST['status']
        Assignment.objects.create(title=title,course=course,subject=subject,due_date=due_date,total_marks=total_marks,attachment=attachment,instructions=instructions,created_by=created_by,status=status)
        messages.success(req,"Assignment uploaded successfully!!")
        return redirect('teacherdash')
    return render(req,"teacher/tchupload_assignment.html")

def tchview_assignment(req):
    assignments=Assignment.objects.all()
    active_count=Assignment.objects.filter(status="Active").count()
    inactive_count=Assignment.objects.filter(status="Inactive").count()
    courses=tbl_course.objects.values_list('course_name',flat=True).distinct()
    context={
        "assignments":assignments,
        "active_count":active_count,
        "inactive_count":inactive_count,
        "courses":courses,
    }
    return render(req,"teacher/tchview_assignment.html",context)

def current_session(req):
    academic_sessions=AcademicSession.objects.all()
    return render(req,"teacher/current_session.html",{"academic_sessions":academic_sessions})

# tbl_student view
def studentdash(req):
    username=tbl_student.objects.get(user=req.user)
    context={
        "username":username,
    }
    return render(req,"student/studentdash.html",context)
# Test the filtter and search using ORM
def filter_test(req):
    teachers=tbl_teacher.objects.all()
    status=req.GET.get('status')
    department=req.GET.get("department")
    if status or department:
        if status:
            teachers=teachers.filter(status=status)
        if department:
            teachers=teachers.filter(department=department)
    context={
        "teachers":teachers,
    }
    return render(req,"admin/filter_test.html",context)

def search_test(req):
    teachers=tbl_teacher.objects.all()
    kwd=req.GET.get('search','').strip()
    print(kwd)
    if kwd:
        teachers=tbl_teacher.objects.filter(name__icontains=kwd)
        if not teachers.exists():
            teachers=tbl_teacher.objects.filter(department__icontains=kwd)
        if not teachers.exists():
            teachers=tbl_teacher.objects.filter(designation__icontains=kwd)
    context={
        "teachers":teachers,
        "kwd":kwd,
    }
    return render(req,"admin/search_test.html",context)

# google meet code 
@login_required
def online_class(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user.is_superuser:
        return redirect('superadmin_schedule_class')
    if hasattr(request.user, 'Teacher'):
        return redirect('teacher_schedule_class')
    return HttpResponse('Only teachers and superadmin can schedule classes.', status=403)


def superadmin_schedule_class(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if not request.user.is_superuser:
        return HttpResponse('Only superadmin can schedule classes.', status=403)
    return render(request, 'admin/onlineclass.html', {
        'teachers': tbl_teacher.objects.select_related('user').order_by('name'),
        'courses': tbl_course.objects.all(),
        'subjects': tbl_subject.objects.all(),
        'fixed_teacher': None,
    })


def teacher_schedule_class(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if not hasattr(request.user, 'Teacher'):
        return HttpResponse('Only teachers can schedule classes.', status=403)
    profile = request.user.Teacher
    return render(request, 'teacher/onlineclass.html', {
        'courses': profile.courses.all() if hasattr(profile, 'courses') else tbl_course.objects.all(),
        'subjects': tbl_subject.objects.all(),
        'fixed_teacher': request.user,
    })


def _refresh_meeting_statuses(queryset):
    from datetime import datetime, timedelta
    from django.utils import timezone
    now = timezone.now()
    for item in queryset.filter(status='live'):
        start = item.started_at
        if not start:
            start = datetime.combine(item.class_date, item.class_time)
            if timezone.is_naive(start):
                start = timezone.make_aware(start, timezone.get_current_timezone())
        if now >= start + timedelta(minutes=item.duration):
            item.status = 'closed'
            item.save(update_fields=['status'])
    return queryset

# def online_class(req):
#     return render(req,"admin/onlineclass.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_code_lab(request):
    context = {
    'languages': LANGUAGES,
    'starter_code': STARTER_CODE,
    }

    return render(
    request,
    'student/code_lab.html',
    context
)
def run_student_code(request):
    language = (request.POST.get('language') or '').strip()
    source_code = request.POST.get('source_code') or ''
    stdin = request.POST.get('stdin') or ''

    if len(source_code) > 50000:
        return JsonResponse({
        'ok': False,
        'error': 'Maximum code size is 50,000 characters.'
    }, status=400)

    if len(stdin) > 10000:
        return JsonResponse({
        'ok': False,
        'error': 'Maximum input size is 10,000 characters.'
    }, status=400)

    result, error = run_code(
    language,
    source_code,
    stdin
)

    if error:
        return JsonResponse({
        'ok': False,
        'error': error
    }, status=502)

    return JsonResponse({
    'ok': True,
    **result
})