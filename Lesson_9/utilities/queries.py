from Lesson_9.utilities import context_manager as cm


class Queries:
    def __init__(self):
        self.db = "students.db"
        self.sql_faculty = "SELECT id FROM faculty WHERE faculty=?"
        self.sql_tutor = "SELECT id FROM tutors WHERE tutor=?"

    def get_all_students(self):
        sql = "SELECT st.id, st.name, st.surname, st.group_num, f.faculty, t.tutor " \
              "FROM students as st " \
              "INNER JOIN faculty as f ON st.faculty_id=f.id " \
              "INNER JOIN tutors as t ON st.tutor_id=t.id"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql).fetchall()
            rows_list = []
            for row in result:
                rows_list.append(dict(zip(row.keys(), tuple(row))))
            return rows_list

    def get_student_by_id(self, student_id):
        sql = "SELECT st.id, st.name, st.surname, st.group_num, f.faculty, t.tutor " \
              "FROM students as st " \
              "INNER JOIN faculty as f ON st.faculty_id=f.id " \
              "INNER JOIN tutors as t ON st.tutor_id=t.id" \
              " WHERE st.id=?"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql, [student_id]).fetchone()
        if result:
            return dict(zip(result.keys(), tuple(result)))
        else:
            return False

    def add_students(self,list_of_dict):
        sql = "INSERT INTO students ('name', 'surname', 'group_num', 'faculty_id', 'tutor_id') VALUES (?,?,?,?,?)"
        for record in list_of_dict:
            try:
                with cm.MyDBManager(self.db, "w") as db:
                    faculty_id = list(db.execute(self.sql_faculty, [record['faculty']]).fetchone())[0]
                    tutor_id = list(db.execute(self.sql_tutor, [record['tutor']]).fetchone())[0]
                    db.executemany(sql, [(record['name'], record['surname'], record['group_num'], faculty_id, tutor_id)])
            except (TypeError, KeyError):
                return False
        return True

    def update_student(self, student_id, student_data):
        sql = "UPDATE students SET name = ?, surname = ?, group_num = ?, faculty_id = ?, tutor_id = ? WHERE id = ?"
        try:
            with cm.MyDBManager(self.db, "w") as db:
                faculty_id = list(db.execute(self.sql_faculty, [student_data['faculty']]).fetchone())[0]
                tutor_id = list(db.execute(self.sql_tutor, [student_data['tutor']]).fetchone())[0]
                db.executemany(sql, [(student_data['name'], student_data['surname'], student_data['group_num'],
                                      faculty_id, tutor_id, student_id)])
        except (TypeError, KeyError):
            return False
        return True

    def delete_student(self, student_id):
        sql_select = "SELECT * FROM students WHERE id = ?"
        sql_delete = "DELETE FROM students WHERE id = ?"
        with cm.MyDBManager(self.db, "w") as db:
            try:
                if db.execute(sql_select, [student_id]).fetchall():
                    db.execute(sql_delete, [student_id]).fetchall()
                    return True
                else:
                    return False
            except (TypeError, KeyError):
                return False

    def get_all_grades(self):
        sql = "SELECT * FROM grades"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql).fetchall()
            rows_list = []
            for row in result:
                rows_list.append(dict(zip(row.keys(), tuple(row))))
            return rows_list

    def get_grades_by_student_id(self, student_id):
        sql = "SELECT * FROM grades WHERE student_id = ?"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql, [student_id]).fetchone()
        if result:
            return dict(zip(result.keys(), tuple(result)))
        else:
            return False

    def add_grades(self, list_of_dict):
        sql = "INSERT INTO grades ('grade', 'subject', 'student_id') VALUES (?,?,?)"
        for record in list_of_dict:
            try:
                with cm.MyDBManager(self.db, "w") as db:
                    db.executemany(sql, [(record['grade'], record['subject'], record['student_id'])])
            except TypeError:
                return False
        return True

    def update_grade(self, grade_id, grade_data):
        sql = "UPDATE grades SET grade = ?, subject = ?, student_id = ? WHERE id = ?"
        try:
            with cm.MyDBManager(self.db, "w") as db:
                db.executemany(sql, [(grade_data['grade'], grade_data['subject'], grade_data['student_id'],
                                      grade_id)])
        except (TypeError, KeyError):
            return False
        return True

    def delete_grade(self, grade_id):
        sql_select = "SELECT * FROM grades WHERE id = ?"
        sql_delete = "DELETE FROM grades WHERE id = ?"
        with cm.MyDBManager(self.db, "w") as db:
            try:
                if db.execute(sql_select, [grade_id]).fetchall():
                    db.execute(sql_delete, [grade_id]).fetchall()
                    return True
                else:
                    return False
            except (TypeError, KeyError):
                return False

    def get_all_tutors(self):
        sql = "SELECT * FROM tutors"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql).fetchall()
            rows_list = []
            for row in result:
                rows_list.append(dict(zip(row.keys(), tuple(row))))
            return rows_list

    def get_tutor_by_id(self, id):
        sql = "SELECT * FROM tutors WHERE id = ?"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql, [id]).fetchone()
        if result:
            return dict(zip(result.keys(), tuple(result)))
        else:
            return False

    def add_tutors(self, list_of_dict):
        sql = "INSERT INTO tutors ('tutor') VALUES (?)"
        for record in list_of_dict:
            try:
                with cm.MyDBManager(self.db, "w") as db:
                    db.execute(sql, [record['tutor']])
            except TypeError:
                return False
        return True

    def update_tutor(self, id, tutor_data):
        sql = "UPDATE tutors SET tutor = ? WHERE id = ?"
        try:
            with cm.MyDBManager(self.db, "w") as db:
                db.executemany(sql, [(tutor_data['tutor'], id)])
        except (TypeError, KeyError):
            return False
        return True

    def delete_tutor(self, id):
        sql_select = "SELECT * FROM tutors WHERE id = ?"
        sql_delete = "DELETE FROM tutors WHERE id = ?"
        with cm.MyDBManager(self.db, "w") as db:
            try:
                if db.execute(sql_select, [id]).fetchall():
                    db.execute(sql_delete, [id]).fetchall()
                    return True
                else:
                    return False
            except (TypeError, KeyError):
                return False

    def get_all_faculties(self):
        sql = "SELECT * FROM faculty"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql).fetchall()
            rows_list = []
            for row in result:
                rows_list.append(dict(zip(row.keys(), tuple(row))))
            return rows_list

    def get_faculty_by_id(self, id):
        sql = "SELECT * FROM faculty WHERE id = ?"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql, [id]).fetchone()
        if result:
            return dict(zip(result.keys(), tuple(result)))
        else:
            return False

    def add_faculties(self, list_of_dict):
        sql = "INSERT INTO faculty ('faculty') VALUES (?)"
        for record in list_of_dict:
            try:
                with cm.MyDBManager(self.db, "w") as db:
                    db.execute(sql, [record['faculty']])
            except TypeError:
                return False
        return True

    def update_faculty(self, id, faculty_data):
        sql = "UPDATE faculty SET faculty = ? WHERE id = ?"
        try:
            with cm.MyDBManager(self.db, "w") as db:
                db.executemany(sql, [(faculty_data['faculty'], id)])
        except (TypeError, KeyError):
            return False
        return True

    def delete_faculty(self, id):
        sql_select = "SELECT * FROM faculty WHERE id = ?"
        sql_delete = "DELETE FROM faculty WHERE id = ?"
        with cm.MyDBManager(self.db, "w") as db:
            try:
                if db.execute(sql_select, [id]).fetchall():
                    db.execute(sql_delete, [id]).fetchall()
                    return True
                else:
                    return False
            except (TypeError, KeyError):
                return False

    def get_excellent_students_by_faculty_id(self, faculty_id):
        sql = "SELECT st.id, st.name, st.surname, st.faculty_id, st.group_num, st.tutor_id " \
              "FROM students as st " \
              "INNER JOIN grades as gr ON st.id=gr.id " \
              "WHERE gr.grade=10 AND st.faculty_id=?"
        with cm.MyDBManager(self.db) as db:
            result = db.execute(sql, [faculty_id]).fetchall()
            rows_list = []
            for row in result:
                rows_list.append(dict(zip(row.keys(), tuple(row))))
                return rows_list
