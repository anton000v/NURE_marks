from django.shortcuts import render, get_object_or_404
from . import models
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render_to_response, HttpResponse


def template_generator_for_user_type(current_user):
    # html_response_template = ''
    # user_type = ''
    if current_user.is_authenticated:
        if current_user.groups.filter(name__in=['Students']).exists():
            html_response_template = 'NURE_marks/students_template.html'
            user_type = 's'
        elif current_user.groups.filter(name__in=['Teachers']).exists():
            html_response_template = 'NURE_marks/teachers_template.html'
            user_type = 't'
        elif current_user.groups.filter(name__in=['Department']).exists():
            html_response_template = 'NURE_marks/department_template.html'
            user_type = 'd'
        else:
            html_response_template = 'NURE_marks/strange_cases_template.html'
            user_type = None
    else:
        html_response_template = 'NURE_marks/not_authenticated_template.html'
        user_type = None
    return user_type, html_response_template


def user_identification(_current_user):
    # student = get_object_or_404(models.Student, pk=current_user.pk)
    current_user = 0
    user_type, html_response_template = template_generator_for_user_type(_current_user)
    if user_type == 's':
        current_user = models.Student.objects.get(student=_current_user)
    elif user_type == 't':
        current_user = models.Teacher.objects.get(teacher=_current_user)
    # elif user_type == 'd':
    #     cur_student = models.De
    return current_user, html_response_template, user_type


def main_screen(request):
    # current_user = request.user
    # html_response_template = template_generator_for_user_type(request.user)
    current_user, html_response_template, user_type = user_identification(request.user)
    if user_type == 's':

    elif
    context = {
        'current_user': current_user,
    }
    return render(request, html_response_template, context)


def user_login(request):
    return render(request, 'Login/login_page.html')
