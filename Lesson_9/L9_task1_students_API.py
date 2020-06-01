"""
Kate Yurmanovych
Lesson 9 Task 1
1) Создать базу данных студентов (ФИО, группа, оценки, куратор студента, факультет).
Написать РЕСТ ко всем сущностям в бд (работа со студентами, оценками, кураторами, факультетами).
Создать отдельные контроллей, который будет выводить отличников по факультету.
"""

from flask import Flask, request, jsonify, make_response
from Lesson_9.utilities import queries as q

app = Flask(__name__)
query = q.Queries()


@app.route('/students', methods=['GET', 'POST'])
@app.route('/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def students(student_id=None):
    if request.method == 'GET':
        data = query.get_all_students()
        if student_id:
            data = query.get_student_by_id(student_id)
            if not data:
                return make_response(jsonify({"Error": "id doesn't exist"}), 422)
        return jsonify(data)

    elif request.method == 'POST':
        if query.add_students(request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({'Error': 'Payload error'}), 422)

    elif request.method == 'PUT':
        if query.update_student(student_id, request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({'Error': 'Payload error'}), 422)

    elif request.method == 'DELETE':
        if query.delete_student(student_id):
            return make_response(jsonify({'Result': 'Success'}), 200)
        else:
            return make_response(jsonify({"Error": "id doesn't exist"}), 422)


@app.route('/grades', methods=['GET', 'POST'])
@app.route('/grades/<int:student_id>', methods=['GET'])
@app.route('/grades/<int:grade_id>', methods=['PUT', 'DELETE'])
def grades(student_id=None, grade_id=None):
    if request.method == 'GET':
        data = query.get_all_grades()
        if student_id:
            data = query.get_grades_by_student_id(student_id)
            if not data:
                return make_response(jsonify({"Error": "can't fetch grades for non-existent student_id"}), 422)
        return jsonify(data)

    elif request.method == 'POST':
        if query.add_grades(request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({'Error': 'Payload error'}), 422)

    elif request.method == 'PUT':
        if query.update_grade(grade_id, request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({"Error": "either id doesn't exist or payload error"}), 422)

    elif request.method == 'DELETE':
        if query.delete_grade(grade_id):
            return make_response(jsonify({'Result': 'Success'}), 200)
        else:
            return make_response(jsonify({"Error": "id doesn't exist"}), 422)


@app.route('/tutors', methods=['GET', 'POST'])
@app.route('/tutors/<int:tutor_id>', methods=['GET', 'PUT', 'DELETE'])
def tutors(tutor_id=None):
    if request.method == 'GET':
        data = query.get_all_tutors()
        if tutor_id:
            data = query.get_tutor_by_id(tutor_id)
            if not data:
                return make_response(jsonify({"Error": "tutor id doesn't exist"}), 422)
        return jsonify(data)

    elif request.method == 'POST':
        if query.add_tutors(request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({'Error': 'Payload error'}), 422)

    elif request.method == 'PUT':
        if query.update_tutor(tutor_id, request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({"Error": "either id doesn't exist or payload error"}), 422)

    elif request.method == 'DELETE':
        if query.delete_tutor(tutor_id):
            return make_response(jsonify({'Result': 'Success'}), 200)
        else:
            return make_response(jsonify({"Error": "id doesn't exist"}), 422)


@app.route('/faculty', methods=['GET', 'POST'])
@app.route('/faculty/<int:faculty_id>', methods=['GET', 'PUT', 'DELETE'])
def faculty(faculty_id=None):
    if request.method == 'GET':
        data = query.get_all_faculties()
        if faculty_id:
            data = query.get_faculty_by_id(faculty_id)
            if not data:
                return make_response(jsonify({"Error": "faculty id doesn't exist"}), 422)
        return jsonify(data)

    elif request.method == 'POST':
        if query.add_faculties(request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({'Error': 'Payload error'}), 422)

    elif request.method == 'PUT':
        if query.update_faculty(faculty_id, request.json):
            return jsonify(request.json)
        else:
            return make_response(jsonify({"Error": "either id doesn't exist or payload error"}), 422)

    elif request.method == 'DELETE':
        if query.delete_faculty(faculty_id):
            return make_response(jsonify({'Result': 'Success'}), 200)
        else:
            return make_response(jsonify({"Error": "id doesn't exist"}), 422)


@app.route('/excellent/<int:faculty_id>')
def excellent_students_by_faculty(faculty_id):
    data = query.get_excellent_students_by_faculty_id(faculty_id)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
