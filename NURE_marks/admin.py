from django.contrib import admin

from .models import Faculty, Specialty, University_Group, Student
from django.contrib.auth.models import User

class Faculty_Admin(admin.ModelAdmin):
    pass


class Specialty_Admin(admin.ModelAdmin):
    pass

class Student_Tabular_Inline(admin.TabularInline):
    model = Student
    extra = 1

class University_Group_Admin(admin.ModelAdmin):
    # raw_id_fields = ("specialty_of_group",)
    inlines = [Student_Tabular_Inline,]
    pass


class Student_Admin(admin.ModelAdmin):
    pass


admin.site.register(Faculty, Faculty_Admin)
admin.site.register(Specialty, Specialty_Admin)

admin.site.register(University_Group, University_Group_Admin)
admin.site.register(Student, Student_Admin)
