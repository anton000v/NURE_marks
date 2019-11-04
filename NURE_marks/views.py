from django.shortcuts import render, get_object_or_404
from . import models
from .forms import DisciplineForGroupMarksForm
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
            user_type = 'sc'
            html_response_template = 'NURE_marks/strange_cases_template.html'
    else:
        user_type = 'na'
        html_response_template = 'NURE_marks/not_authenticated_template.html'
    return user_type, html_response_template


def user_identification(_current_user):
    # student = get_object_or_404(models.Student, pk=current_user.pk)
    current_user = ''
    user_type, html_response_template = template_generator_for_user_type(_current_user)
    if user_type == 's':
        current_user = models.Student.objects.get(student=_current_user)
    elif user_type == 't':
        current_user = models.Teacher.objects.get(teacher=_current_user)
    # elif user_type == 'd':
    #     cur_student = models.De
    return current_user, html_response_template, user_type


def student_views():
    return 0


def main_screen(request):
    # current_user = request.user
    # html_response_template = template_generator_for_user_type(request.user)
    current_user, html_response_template, user_type = user_identification(request.user)
    context = {
        'current_user': current_user,
    }

    if user_type == 's':
        # student_group = models.University_Group.objects.get(pk=current_user.student_group.pk)
        # print(student_group)
        disciplines_for_current_group = models.DisciplineForGroup.objects.all().filter(group=current_user.student_group)
        # group_marks = models.Mark.objects.all().filter(group=current_user.student_group)
        # for d in group_marks:
        #     print(d.student, ' - ', d.subject, d.marks)
        context['student_group'] = current_user.student_group
        context['disciplines_for_current_group'] = disciplines_for_current_group
        # context['group_marks'] = group_marks
    elif user_type == 't':

        # for dicipline in models.Subject.objects.all().filter(lecturer=current_user.teacher)
        lecture_disciplines = models.Subject.objects.all().filter(lecturer=current_user)

        # groups_of_lectures = []
        # for discipline in lecture_disciplines:
        #     groups_of_lectures += models.DisciplineForGroup.objects.all().filter(subject=discipline)
        # print(groups_of_lectures)

        subject_query = request.GET.get('teacher-subject-select')
        teacher_subject_groups = []
        if subject_query != '' and subject_query is not None:
            teacher_subject_groups = models.DisciplineForGroup.objects.all().filter(
                subject=subject_query)
        print(teacher_subject_groups)
        context['lecture_disciplines'] = lecture_disciplines
        context['teacher_subject_groups'] = teacher_subject_groups
        if subject_query:
            context['subject_query'] = int(subject_query)
        # return render(request, 'NURE_marks/teachers_template.html', context)
    # elif user_type == 't':
    #     # return render(request,'NURE_marks/department_template.html',context)
    # elif user_type == 'sc':
    #     # return render(request, 'NURE_marks/strange_cases_template.html', context)
    # elif user_type == 'na':
    #     # return render(request, 'NURE_marks/strange_cases_template.html', context)
    # elif user_type == 't':
    #     context += {'':}
    return render(request, html_response_template, context)


def group_detail(request, group_pk, subject_pk):
    group = get_object_or_404(models.University_Group, pk=group_pk)
    subject = get_object_or_404(models.Subject, pk=subject_pk)
    print(group)
    # disciplines_for_current_group = models.DisciplineForGroup.objects.all().filter(group=group)
    group_marks = models.Mark.objects.all().filter(subject=subject_pk)
    print(group_marks)
    # context = dict([])
    # context['student_group'] = group
    # context['disciplines_for_current_group'] = disciplines_for_current_group
    # context['group_marks'] = group_marks
    context = {
        'group': group,
        'group_marks': group_marks,
        'subject': subject,
    }
    return render(request, 'NURE_marks/group_detail.html', context)


def group_marks_edit(request, group_pk, subject_pk):
    group = get_object_or_404(models.University_Group, pk=group_pk)
    subject = get_object_or_404(models.Subject, pk=subject_pk)
    group_discipline = get_object_or_404(models.DisciplineForGroup, pk=subject_pk)
    group_marks = models.Mark.objects.all().filter(subject=subject_pk)

    form = DisciplineForGroupMarksForm(instance=group_discipline)
    context = {
        'group': group,
        'group_marks': group_marks,
        'subject': subject,
        'group_discipline':group_discipline,
        'form':form,
    }
    return render(request, 'NURE_marks/group_marks_edit.html', context)


def user_login(request):
    return render(request, 'Login/login_page.html')
