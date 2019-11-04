from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import DisciplineForGroup


class DisciplineForGroupMarksForm(forms.ModelForm):
    class Meta:
        model = DisciplineForGroup

        # Возможно, филдсет не нужен
        fields = (
        'number_of_lectures', 'number_of_practical_lessons', 'number_of_laboratory_lessons', 'number_of_tests',
        'number_of_home_works', 'course_work')
        exclude = ()
