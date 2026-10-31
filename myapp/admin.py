from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AcademicSession)
admin.site.register(tbl_course)
admin.site.register(tbl_teacher)
admin.site.register(tbl_subject)
admin.site.register(tbl_student)
admin.site.register(StudyMaterial)
admin.site.register(Assignment)
admin.site.register(Attendance)
