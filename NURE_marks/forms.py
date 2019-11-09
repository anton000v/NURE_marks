from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import DisciplineForGroup, Mark


class DisciplineForGroupMarksForm(forms.ModelForm):
    class Meta:
        model = DisciplineForGroup

        # Возможно, филдсет не нужен
        fields = (
            'number_of_lectures', 'number_of_practical_lessons', 'number_of_laboratory_lessons', 'number_of_tests',
            'number_of_home_works', 'course_work')
        exclude = ()


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('mark','student')
        # exclude = ()
    # def __init__(self, *args, **kwargs):
    #     super(MarkForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         self.fields['type_of_mark'].widget.attrs['readonly'] = True
    #
    # def __init__(self, *args, **kwargs):
    #     super(MarkForm, self).__init__(*args, **kwargs)
    # self.fields['type_of_mark'].disabled = True
    # self.fields['student'].disabled = True
    # self.fields['number_of_type_of_mark'].disabled = True
    # def __init__(self, *args, **kwargs):
    #     super(MarkForm, self).__init__(*args, **kwargs)
    #     if self.instance.id:
    #         self.fields['type_of_mark'].widget.attrs['readonly'] = True
    #         self.fields['number_of_type_of_mark'].widget.attrs['readonly'] = True

# class MarksForm(forms.ModelForm):
#     class Meta:
#         model = Mark
#
#         fields = (
#             'student',
#             'marks',
#         )
#         readonly_fields = ('marks',)
#         exclude = ()
