LECTURE = 'le'
PRACTICAL_LESSON = 'pl'
LABORATORY_LESSON = 'lw'
TEST = 'te'
HOME_WORK = 'hw'
COURSE_WORK = 'cw'

# TYPE_OF_MARK_CHOICES = [
#     ('Лекция', LECTURE),
#     ('Лабораторна', LABORATORY_LESSON),
#     ('Практическое занятие', PRACTICAL_LESSON),
#     ('Тест', TEST),
#     ('Домашнее занятие', HOME_WORK),
#     ('Курсовая работа', COURSE_WORK),
# ]

TYPE_OF_MARK_CHOICES = [
    (LECTURE, 'Лекция'),
    (LABORATORY_LESSON, 'Лабораторная работа'),
    (PRACTICAL_LESSON, 'Практическое занятие'),
    (TEST, 'Тест'),
    (HOME_WORK, 'Домашнее занятие'),
    (COURSE_WORK, 'Курсовая работа'),
]


matching_numbers_and_names = dict()
for key, value in (
        ('number_of_lectures', LECTURE), ('number_of_practical_lessons', PRACTICAL_LESSON),
        ('number_of_laboratory_lessons', LABORATORY_LESSON), ('number_of_tests', TEST),
        ('number_of_home_works', HOME_WORK), ('course_work', COURSE_WORK)):
    matching_numbers_and_names[key] = value
# NUMBER_OF_LESSONS_CHOICES = {
#     'number_of_lectures':,
# 'number_of_lectures': ,
# 'number_of_lectures': ,
# 'number_of_lectures': ,
# 'number_of_lectures': ,
# 'number_of_lectures': ,
# }
