from django.contrib import admin

from .models import Faculty, Specialty, University_Group, Student, Subject, Mark, DisciplineForGroup
from django.contrib.auth.models import User


class FacultyAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'smart-selects/admin/js/chainedfk.js',
            'smart-selects/admin/js/chainedm2m.js',
        )


class StudentTabularInline(admin.TabularInline):
    model = Student
    extra = 1


class UniversityGroupAdmin(admin.ModelAdmin):
    # raw_id_fields = ("specialty_of_group",)
    inlines = [StudentTabularInline, ]
    pass


class StudentAdmin(admin.ModelAdmin):
    pass


class MarkTabularInline(admin.TabularInline):
    model = Mark


class SubjectAdmin(admin.ModelAdmin):
    pass


class DisciplineForGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)

admin.site.register(University_Group, UniversityGroupAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(DisciplineForGroup,DisciplineForGroupAdmin)