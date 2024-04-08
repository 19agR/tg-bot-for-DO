import sqlite3


class CoursesDataBase:
    def __init__(self, path):
        self.path = path
        self.quantity_courses = self.get_quantity_courses()

    def connect(self):
        return sqlite3.connect(self.path)

    def execute(self, query, data=tuple(), fetchall=False, fetchone=False):
        con = self.connect()

        cursor = con.cursor()
        result = cursor.execute(query, data)

        if fetchall:
            return result.fetchall()
        elif fetchone:
            return result.fetchone()

        con.commit()
        con.close()

    def create_tables(self):
        query_teachers = """
        CREATE TABLE IF NOT EXISTS Teachers (
        'id Преподавателя' INTEGER PRIMARY KEY AUTOINCREMENT,
        ФИО TEXT NOT NULL,
        'Номер телефона' TEXT NOT NULL
        )
        """
        self.execute(query_teachers)

        query_courses = """
        CREATE TABLE IF NOT EXISTS Courses (
        'id Курса' INTEGER PRIMARY KEY AUTOINCREMENT,
        'id Преподавателя' INTEGER,
        Название TEXT NOT NULL,
        Описание TEXT NOT NULL,
        'Стоимость в месяц' INTEGER NOT NULL,
        'Тип курса' TEXT NOT NULL,
        'Доступных мест' TEXT,
        'Расписание' TEXT,
        FOREIGN KEY ('id Преподавателя') REFERENCES Teachers ('id Преподавателя')
        )
        """
        self.execute(query_courses)

        query_students = """
        CREATE TABLE IF NOT EXISTS Students (
        'id Ученика' INTEGER PRIMARY KEY AUTOINCREMENT,
        ФИО TEXT NOT NULL,
        'Номер телефона' TEXT NOT NULL,
        'tg_user_id' INTEGER NOT NULL,
        'tg_username' INTEGER NOT NULL,
        'Выбранные курсы' TEXT
        )
        """
        self.execute(query_students)

    def add_course_to_user(self, data: dict):
        """
        format for param data: {
            'full_name',
            'phone_number',
            'tg_user_id',
            'tg_username',
            'selected_course'
        }
        """

        try:
            full_name = data['name']
            phone_number = data['phone_number']
            tg_user_id = data['tg_user_id']
            tg_username = data['tg_username']
            selected_course = data['course_id']

            if not isinstance(full_name, str) or not isinstance(phone_number, str):
                raise KeyError()

        except KeyError:
            print('Ошибка формата переданных данных для добавления курса к ученику')
            return False

        query = ("INSERT INTO Students (ФИО, [Номер телефона], tg_user_id, tg_username, [Выбранные курсы]) "
                 "VALUES (?, ?, ?, ?, ?)")
        self.execute(query, data=(full_name, phone_number, tg_user_id, tg_username, selected_course))

        return True


    def add_teacher(self, data: dict):
        """
        format for param data: {
            'full_name',
            'phone_number'
        }
        """

        try:
            full_name = data['full_name']
            phone_number = data['phone_number']

            if not isinstance(full_name, str) or not isinstance(phone_number, str):
                raise KeyError()

        except KeyError:
            print('Ошибка формата переданных данных для добавления учителя')
            return False

        query = "INSERT INTO Teachers (ФИО, [Номер телефона]) VALUES (?, ?)"
        self.execute(query, data=(full_name, phone_number))

        return True

    def add_course(self, data: dict):
        """
        format for param data: {
            'teacher_id'
            'name',
            'description',
            'cost_per_month',
            'type_course',
            'available_places',
            'timetable'
        }
        """

        try:
            teacher_id = data['teacher_id']
            name = data['name']
            description = data['description']
            cost_per_month = data['cost_per_month']
            type_course = data['type_course']
            available_places = data['available_places']
            timetable = data['timetable']
        except KeyError:
            print('Ошибка формата переданных данных для добавления курса')
            return

        query = """
        INSERT INTO Courses (
        [id Преподавателя], Название, Описание,
        [Стоимость в месяц], [Тип курса], [Доступных мест], Расписание
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(query,
                     data=(teacher_id, name, description, cost_per_month, type_course, available_places, timetable))
        self.quantity_courses += 1

    def redact_course(self, data):
        course_id = data['course_id']
        teacher_id = data['teacher_id']
        name = data['name']
        description = data['description']
        cost_per_month = data['cost_per_month']
        type_course = data['type_course']
        available_places = data['available_places']
        timetable = data['timetable']
        query = f"""
                UPDATE Courses SET
                [id Преподавателя]='{teacher_id}',
                Название='{name}',
                Описание='{description}',
                [Стоимость в месяц]='{cost_per_month}',
                [Тип курса]='{type_course}',
                [Доступных мест]='{available_places}',
                Расписание='{timetable}'
                WHERE [id Курса] = {course_id}
                """
        self.execute(query)

    def select_courses(self):
        query = "SELECT * FROM Courses"
        return self.execute(query, fetchall=True)

    def select_course(self, course_id):
        query = f"SELECT * FROM Courses WHERE [id Курса] = {course_id}"
        return self.execute(query, fetchone=True)

    def select_teacher(self, teacher_id):
        query = f"SELECT * FROM Teachers WHERE [id Преподавателя] = {teacher_id}"
        return self.execute(query, fetchone=True)

    def select_teachers(self):
        query = f"SELECT * FROM Teachers"
        return self.execute(query, fetchall=True)

    def get_quantity_courses(self):
        return len(self.execute('SELECT * FROM Courses', fetchall=True))


db = None  # need to pass import error
if __name__ == '__main__':
    db = CoursesDataBase('../data/courses_db.sqlite3')
    print(db.select_courses())
    db.create_tables()
else:
    db = CoursesDataBase('data/courses_db.sqlite3')  # this is needed to be able to open db from other files

