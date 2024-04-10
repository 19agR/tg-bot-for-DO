from utils.db import db


def pages_info(n):
    return f'{n}/{db.quantity_courses}'


def print_course(course):
    teacher_id = course[1]
    teacher_name = db.select_teacher(teacher_id)[1]
    name = course[2]
    description = course[3]
    cost_per_month = course[4]
    type_course = course[5]
    available_places = course[6]
    timetable = course[7]

    available_places = f'<b><i>Доступных мест:</i></b>  {available_places}\n' if available_places not in [None, 'None'] else ''
    timetable = f'<b><i>Расписание занятий:</i></b>\n{timetable}\n' if timetable not in [None, 'None'] else ''

    prepared_text = (f'<b><u>Информация о курсе</u></b>\n\n'
                     f'<b><i>Название:</i></b>  {name}\n'
                     f'<b><i>Описание:</i></b>  {description}\n'
                     f'<b><i>Преподаватель:</i></b>  {teacher_name}\n'
                     f'<b><i>Стоимость в месяц:</i></b>  {cost_per_month}₽\n'
                     f'<b><i>Тип курса:</i></b>  {type_course}\n' + available_places + timetable)

    return prepared_text


