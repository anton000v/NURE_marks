# Generated by Django 2.2.5 on 2019-10-07 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NURE_marks', '0004_university_group_course_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='university_group',
            name='course_number',
        ),
        migrations.AddField(
            model_name='university_group',
            name='year_of_receipt',
            field=models.PositiveSmallIntegerField(default=2019),
        ),
    ]
