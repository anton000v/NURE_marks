from django.shortcuts import render, get_object_or_404
from . import models
from .forms import DisciplineForGroupMarksForm, MarkForm
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render_to_response, HttpResponse
from django.forms import modelformset_factory, inlineformset_factory
from . import choices


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
        teacher_discipline_groups = []
        if subject_query != '' and subject_query is not None:
            teacher_discipline_groups = models.DisciplineForGroup.objects.all().filter(
                subject=subject_query)
        print(teacher_discipline_groups)
        context['lecture_disciplines'] = lecture_disciplines
        context['teacher_discipline_groups'] = teacher_discipline_groups
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


def group_detail(request, group_pk, discipline_pk):
    group = get_object_or_404(models.University_Group, pk=group_pk)
    group_discipline = get_object_or_404(models.DisciplineForGroup, pk=discipline_pk)
    # print(group)
    # disciplines_for_current_group = models.DisciplineForGroup.objects.all().filter(group=group)

    group_marks = models.Mark.objects.all().filter(discipline=discipline_pk)

    for mark in group_marks:
        if mark.student.student_group.pk != group.pk:
            print("ОШИБКА, студент", mark.student, "не учится в группе", group, ', но получил оценку по предмету "',
                  group_discipline, '",как член этой группы.')
    print(discipline_pk)

    # print(group_marks)
    # context = dict([])
    # context['student_group'] = group
    # context['disciplines_for_current_group'] = disciplines_for_current_group
    # context['group_marks'] = group_marks
    context = {
        'group': group,
        'group_marks': group_marks,
        'group_discipline': group_discipline,
    }
    return render(request, 'NURE_marks/group_detail.html', context)


def get_dict_with_numbers_of_works_of_group_discipline(group_discipline):
    number_of_lectures = group_discipline.number_of_lectures
    number_of_laboratory_lessons = group_discipline.number_of_laboratory_lessons
    number_of_practical_lessons = group_discipline.number_of_practical_lessons
    number_of_home_works = group_discipline.number_of_home_works
    number_of_tests = group_discipline.number_of_tests
    course_work = group_discipline.course_work
    return {'number_of_lectures': number_of_lectures, 'number_of_laboratory_lessons': number_of_laboratory_lessons,
            'number_of_practical_lessons': number_of_practical_lessons,
            'number_of_home_works': number_of_home_works,
            'number_of_tests': number_of_tests,
            'course_work': course_work}


def group_marks_edit(request, group_pk, discipline_pk):
    group = get_object_or_404(models.University_Group, pk=group_pk)

    group_discipline = get_object_or_404(models.DisciplineForGroup, pk=discipline_pk)
    group_marks = models.Mark.objects.all().filter(discipline=discipline_pk)

    group_marks_formset_model = inlineformset_factory(models.DisciplineForGroup, models.Mark,
                                                      # fields=(
                                                      #     'student', 'marks', 'type_of_mark', 'number_of_type_of_mark'),
                                                      extra=0,
                                                      can_delete=True,
                                                      form=MarkForm,
                                                      )

    old_numbers_of_works_info = get_dict_with_numbers_of_works_of_group_discipline(group_discipline=group_discipline)
    # works_info_for_table = {key: range(1, old_numbers_of_works_info[key] + 1) for key in
    #                         old_numbers_of_works_info.keys()}
    # print(works_info_for_table.items())
    works_info_for_table = []

    for key, value in old_numbers_of_works_info.items():
        if value > 0:
            if key == 'number_of_lectures':
                works_info_for_table.append(('Лекция', range(1, value + 1), choices.matching_numbers_and_names[key]), )
            elif key == 'number_of_laboratory_lessons':
                works_info_for_table.append(
                    ('Лабораторная работа', range(1, value + 1), choices.matching_numbers_and_names[key]), )
            elif key == 'number_of_practical_lessons':
                works_info_for_table.append(('Практическая работа', range(1, value + 1),choices.matching_numbers_and_names[key]), )
            elif key == 'number_of_home_works':
                works_info_for_table.append(('Домашная работа', range(1, value + 1),choices.matching_numbers_and_names[key]), )
            elif key == 'number_of_tests':
                works_info_for_table.append(('Тест', range(1, value + 1),choices.matching_numbers_and_names[key]), )
            elif key == 'course_work':
                works_info_for_table.append(('Курсовая работа', None,choices.matching_numbers_and_names[key]), )
    print(works_info_for_table)
    # for key, value in (
    #         ('number_of_lectures', LECTURE), ('number_of_practical_lessons', PRACTICAL_LESSON),
    #         ('number_of_laboratory_lessons', LABORATORY_LESSON), ('number_of_tests', TEST),
    #         ('number_of_home_works', HOME_WORK), ('course_work', COURSE_WORK)):
    #     matching_numbers_and_names[key] = value
    print('старое число работ: ', old_numbers_of_works_info)
    if request.method == "POST":
        discipline_form = DisciplineForGroupMarksForm(request.POST or None, instance=group_discipline)
        group_marks_formset = group_marks_formset_model(request.POST or None, instance=group_discipline,
                                                        prefix='group_marks')

        # print(discipline_form.is_valid(), group_marks_formset.is_valid())
        if discipline_form.is_valid() and group_marks_formset.is_valid():
            # number_of_lectures = int(discipline_form.cleaned_data['number_of_lectures'])
            new_numbers_of_works_info = discipline_form.cleaned_data
            changed_values_of_works_info = dict(
                [x for x in new_numbers_of_works_info.items() if x not in old_numbers_of_works_info.items()])

            print('Новое число работ:', new_numbers_of_works_info)
            print('измененные значения', changed_values_of_works_info)
            print('2 вариант пересечения: ',
                  dict(old_numbers_of_works_info.items() & new_numbers_of_works_info.items()))

            for key, value in changed_values_of_works_info.items():
                if value > old_numbers_of_works_info[key]:
                    for i in range(old_numbers_of_works_info[key] + 1, value + 1):
                        for student in group_discipline.group.student_group.all():
                            new_mark = models.Mark(discipline=group_discipline, student=student,
                                                   type_of_mark=choices.matching_numbers_and_names[key],
                                                   number_of_type_of_mark=i, mark=0)
                            new_mark.save()
                elif value < old_numbers_of_works_info[key]:
                    for i in range(value + 1, old_numbers_of_works_info[key] + 1, ):
                        for student in group_discipline.group.student_group.all():
                            # new_mark = models.Mark(discipline=group_discipline, student=student,
                            #                        type_of_mark=choices.matching_numbers_and_names[key],
                            #                        number_of_type_of_mark=i, marks=0)
                            models.Mark.objects.filter(discipline=group_discipline, student=student,
                                                       type_of_mark=choices.matching_numbers_and_names[key],
                                                       number_of_type_of_mark=i).delete()
                            # new_mark.save()
            # if group_discipline.number_of_lectures != number_of_lectures:
            #     for i in range(1, number_of_lectures + 1):
            #         for student in group_discipline.group.student_group.all():
            #             new_mark = models.Mark(discipline=group_discipline, student=student,
            #                                    type_of_mark=choices.LABORATORY_LESSON,
            #                                    number_of_type_of_mark=i, marks=0)
            #             new_mark.save()
            # print(new_mark)
            discipline_form.save()
            group_marks_formset.save()
            return redirect('group_detail', group_pk=group_pk, discipline_pk=discipline_pk)


    else:
        discipline_form = DisciplineForGroupMarksForm(instance=group_discipline)
        group_marks_formset = group_marks_formset_model(instance=group_discipline, prefix='group_marks')
    context = {
        'group': group,
        'group_marks': group_marks,
        # 'subject': subject,
        'group_discipline': group_discipline,
        'discipline_form': discipline_form,
        'group_marks_formset': group_marks_formset,
        'works_info_for_table': works_info_for_table,
    }
    # for form in group_marks_formset.forms:
    #     print(form.student)
    return render(request, 'NURE_marks/group_marks_edit.html', context)


def user_login(request):
    return render(request, 'Login/login_page.html')
