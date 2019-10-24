from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render_to_response, HttpResponse


def template_generator_for_user_type(current_user):
    html_response_template = ''
    if current_user.is_authenticated:
        if current_user.groups.filter(name__in=['Students']).exists():
            html_response_template = 'NURE_marks/students_template.html'
        elif current_user.groups.filter(name__in=['Teachers']).exists():
            html_response_template = 'NURE_marks/teachers_template.html'
        elif current_user.groups.filter(name__in=['Department']).exists():
            html_response_template = 'NURE_marks/department_template.html'
        else:
            html_response_template = 'NURE_marks/strange_cases_template.html'
    else:
        html_response_template = 'NURE_marks/not_authenticated_template.html'
    return html_response_template


def main_screen(request):
    current_user = request.user
    html_response_template = template_generator_for_user_type(current_user)

    return render(request, html_response_template)


def user_login(requset):
    return render(requset, 'Login/login_page.html')
