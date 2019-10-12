from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
import datetime
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.

# ------пока не юзаю
# class Users(models.Model):
#     STUDENT = 's'
#     TEACHER = 't'
#     DEPARTMENT = 'd'
#     USER_TYPE_CHOICES = (
#         (STUDENT, 'Студент'),
#         (TEACHER, 'Преподаватель'),
#         (DEPARTMENT, 'Департамент'),
#     )
#     email = models.EmailField(max_length=50)
#     password = models.CharField(max_length=100)
#     user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)


# class University_Groups(models.Model):
#     name = models.CharField(max_length=100)
#     students = models.ManyToOneRel(
#         User,
#         on_delete=models.CASCADE,
#     )

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=5, verbose_name="Название факультета")

    # def(self,str):
    #     queryset = self.objects.
    def __str__(self):
        return self.faculty_name


class Specialty(models.Model):
    faculty_name_of_specialty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Выберите факультет")
    specialty_name = models.CharField(max_length=50, verbose_name="Название специальности")

    def __str__(self):
        return self.specialty_name


# class Course(models.Model):
#     course_number = models.PositiveSmallIntegerField()
#     specialty_name_of_course = models.ForeignKey(Specialty, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{} курс'.format(self.course_number)


class University_Group(models.Model):
    group_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Факультет группы")
    # specialty_of_group = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name="Выберите специальность",
    #                                        # limit_choices_to={'id__in': Faculty}
    #                                        )
    specialty_of_group = ChainedForeignKey(
        Specialty,
        chained_field="group_faculty",
        chained_model_field="faculty_name_of_specialty",
        show_all=False,
        auto_choose=True
    )
    group_number = models.PositiveSmallIntegerField(verbose_name='Номер группы')
    year_of_receipt = models.PositiveSmallIntegerField(default=datetime.date.today().year,
                                                       verbose_name="Год начала обучения")

    # student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Students"})

    def __str__(self):
        return "%s%s-%i-%i" % (
            self.group_faculty, self.specialty_of_group, abs(self.year_of_receipt) % 100, self.group_number)


class Student(models.Model):
    student_group = models.ForeignKey(University_Group, on_delete=models.CASCADE, related_name='student_group')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Students"},
                                null=True, blank=True)

    def __str__(self):
        return self.student.get_username()

# ---------------------------------------- Example multi fields django smart selects
# class Continent(models.Model):
#     continent = models.CharField(max_length=45)
#
#     def __str__(self):
#         return self.continent
#
#
# class Country(models.Model):
#     continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
#     country = models.CharField(max_length=45)
#
#     def __str__(self):
#         return self.country
#
# class Area(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     area = models.CharField(max_length=45)
#
#     def __str__(self):
#         return self.area
#
#
# class Location(models.Model):
#     continent = models.ForeignKey(Continent, on_delete=models.CASCADE,verbose_name='Континент')
#     country = ChainedForeignKey(
#         Country,
#         chained_field="continent",
#         chained_model_field="continent",
#         show_all=False,
#         auto_choose=True
#     )
#     area = ChainedForeignKey(Area, chained_field="country", chained_model_field="country")
#     city = models.CharField(max_length=50)
#     street = models.CharField(max_length=100)
