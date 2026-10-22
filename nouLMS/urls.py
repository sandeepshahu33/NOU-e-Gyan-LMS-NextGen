"""
URL configuration for nouLMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('admindash/',admindash,name='admindash'),
    path('add_session/',add_session,name='add_session'),
    path('view_sessions/',view_sessions,name='view_sessions'),
    path('edit_session/<id>/',edit_session,name='edit_session'),
    path('delete_session/<id>/',delete_session,name='delete_session'),
    path('add_course/',add_course,name='add_course'),
    path('edit_course/<id>/',edit_course,name='edit_course'),
    path('delete_course/<id>/',delete_course,name='delete_course'),
    path('view_courses/',view_courses,name='view_courses'),

    path('add_teacher/',add_teacher,name='add_teacher'),
    path('view_teacher/',view_teacher,name='view_teacher'),
    path('edit_teacher/<id>/',edit_teacher,name='edit_teacher'),
    path('delete_teacher/<id>/',delete_teacher,name='delete_teacher'),


    path('add_subject/',add_subject,name='add_subject'),
    path('view_subjects/',view_subjects,name='view_subjects'),

    path('add_student/',add_student,name='add_student'),
    path('view_students/',view_students,name='view_students'),
    path('view_students/',view_students,name='view_students'),
    path('edit_student/<id>/',edit_student,name='edit_student'),
    path('delete_student/<id>/',delete_student,name='delete_student'),

    path('add_studymaterial/',add_studymaterial,name='add_studymaterial'),
    path('view_studymaterial/',view_studymaterial,name='view_studymaterial'),
    path('edit_studymaterial/<id>/',edit_studymaterial,name='edit_studymaterial'),
    path('delete_studymaterial/<id>/',delete_studymaterial,name='delete_studymaterial'),

    path('upload_assignment/',upload_assignment,name='upload_assignment'),
    path('view_assignment/',view_assignment,name='view_assignment'),
    path('edit_assignment/<id>/',edit_assignment,name='edit_assignment'),
    path('delete_assignment/<id>/',delete_assignment,name='delete_assignment'),

    # Teacher ulrls
    path('teacherdash/',teacherdash,name='teacherdash'),
    # Student urls
    path('studentdash/',studentdash,name='studentdash'),
    path('logout/',user_logout,name='logout'),
]

if settings.DEBUG:urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
