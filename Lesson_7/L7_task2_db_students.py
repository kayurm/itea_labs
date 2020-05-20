"""
Kate Yurmanovych
Lesson 7 Task 2
2) Создать базу данных студентов. У студента есть факультет,
группа, оценки, номер студенческого билета. Написать программу,
с двумя ролями: Администратор, Пользователь. Администратор
может добавлять, изменять существующих студентов.
Пользователь может получать список отличников, список всех
студентов, искать студентов по по номеру студенческого, получать
полную информацию о конкретном студенте (включая оценки,
факультет)
"""

from Lesson_7 import L7_task1_db_context_manager as cm


class StandardUser:

    @classmethod
    def get_all_students(cls):
        sql = "SELECT * FROM students"
        with cm.MyDBManager("students.db") as db:
            db.execute(sql)
            return db.fetchall()

    @classmethod
    def get_all_excellent_students(cls):
        sql = "SELECT students.name,students.surname FROM students INNER JOIN grades " \
              "ON students.id = grades.student_id WHERE grades.marks = 10"
        with cm.MyDBManager("students.db") as db:
            db.execute(sql)
            return db.fetchall()

    @classmethod
    def is_student_by_id(cls, student_id):
        sql = "select * from students where id = ?"
        with cm.MyDBManager("students.db") as db:
            result = db.execute(sql, [student_id])
            return True if result is not None else False

    @classmethod
    def get_full_student_info_by_id(cls, student_id):
        sql = "SELECT students.id, students.name,students.surname, faculty.faculty_name, subjects.subject_name, grades.marks " \
              "FROM students INNER JOIN faculty on students.faculty_id=faculty.faculty_id " \
              "INNER JOIN grades on students.id = grades.student_id " \
              "INNER JOIN subjects on grades.subject_id = subjects.subject_id WHERE students.id = ?"
        with cm.MyDBManager("students.db") as db:
            db.execute(sql, [student_id])
            return db.fetchall()


class Admin:

    @classmethod
    def add_student(cls, name, surname, faculty_id, group_id):
        sql = "INSERT INTO students ('name', 'surname', 'faculty_id', 'group_id') VALUES (?,?,?,?)"
        with cm.MyDBManager("students.db") as db:
            db.executemany(sql, [(name, surname, faculty_id, group_id)])

    @classmethod
    def modify_student(cls, student_id, name, surname, faculty_id, group_id):
        sql = "UPDATE students SET name = ?, surname = ?, faculty_id = ?, group_id = ? WHERE id = ?;"
        with cm.MyDBManager("students.db") as db:
            db.executemany(sql, [(name, surname, faculty_id, group_id, student_id)])
            return db.fetchall()


if __name__ == "__main__":
    st_user = StandardUser()
    print("All students list:\n", st_user.get_all_students())
    print("All excellent students list:\n", st_user.get_all_excellent_students())
    st_id = 1
    print(f"Is there a student by their id '{st_id}':", st_user.is_student_by_id(st_id))
    st_id = 2
    print(f"Full info on student with id '{st_id}':\n", st_user.get_full_student_info_by_id(st_id))

    admin = Admin()
    admin.add_student("Gonzalez", "Guringa", 1, 2)
    admin.modify_student(1, "New_name", "New_surname", 3, 3)
    # to check up:
    print("All students list:\n", st_user.get_all_students())
