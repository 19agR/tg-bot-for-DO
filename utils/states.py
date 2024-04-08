from aiogram.fsm.state import StatesGroup, State


class AddNewTeacher(StatesGroup):
    full_name = State()
    phone_number = State()
    accept = State()


class CreateCourse(StatesGroup):
    teacher_id = State()
    name = State()
    description = State()
    cost_per_month = State()
    type_course = State()
    available_places = State()
    timetable = State()
    accept = State()


class SelectCourseByUser(StatesGroup):
    full_name = State()
    phone_number = State()
    accept = State()
