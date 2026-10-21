from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AcademicSession)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(StudyMaterial)
