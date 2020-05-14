"""Kateryna Yurmanovych
     lesson 4
     Task 1

Создайте класс ПЕРСОНА с абстрактными методами, позволяющими
вывести на экран информацию о персоне, а также определить ее возраст (в
текущем году). Создайте дочерние классы: АБИТУРИЕНТ (фамилия, дата
рождения, факультет), СТУДЕНТ (фамилия, дата рождения, факультет, курс),
ПРЕПОДАВАТЕЛЬ (фамилия, дата рождения, факультет, должность, стаж),
со своими методами вывода информации на экран и определения возраста.
Создайте список из n персон, выведите полную информацию из базы на
экран, а также организуйте поиск персон, чей возраст попадает в заданный
диапазон.
"""

"""
I've created two main classes - Library and abstract Person. Library is a 
singleton and used for storing data of the instances of classes-heirs of Person, such as Enrollee, Student and Teacher.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class LibrarySingleton:
    instance = None
    _id = 0
    _people_dict = dict()

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        cls.instance = super().__new__(cls)
        return cls.instance

    def add_record(self, person_in: object):
        LibrarySingleton._id += 1
        self._people_dict[LibrarySingleton._id] = person_in

    def get_record(self, record_id):
        return self._people_dict[record_id]

    def print_all_records(self):
        for key in self._people_dict:
            self._people_dict[key].print_info()

    def print_records_by_age_range(self, start: float, end: float):
        print(50 * "W", f"\nPeople whose age is in the range {start} - {end}")
        for key in self._people_dict:
            age = self._people_dict[key].age
            if start < age < end:
                self._people_dict[key].print_info()


class Person(ABC):
    """
    date of birth (dob) should be in the exact format: str: “dd/mm/YYYY”
    """

    @abstractmethod
    def __init__(
            self,
            full_name: str = None,
            date_of_birth: str = None):
        self.name = full_name if full_name else "Not given"
        try:
            self.dob = datetime.strptime(date_of_birth, '%d/%m/%Y')
        except (TypeError, ValueError):
            print('\nException: Incorrect D.O.B. format, should be string “dd/mm/YYYY”. \nYour D.O.B. will be set to '
                  '01/01/1900')
            self.dob = datetime.strptime("01/01/1900", '%d/%m/%Y')
        self.person_type = None
        self.library = LibrarySingleton()
        self.library.add_record(self)

    @property
    def age(self):
        age = round((datetime.now() - self.dob).days / 365, 2)
        return age

    @abstractmethod
    def print_info(self):
        print(50 * '*')
        print('Full name: ', self.name)
        print('Age: ', self.age)
        print('Type: ', self.person_type)


class Enrollee(Person):

    def __init__(
            self,
            full_name: str = None,
            date_of_birth: str = None,
            faculty: str = None):
        super().__init__(full_name, date_of_birth)
        self.faculty = faculty if faculty else "Not given"
        self.person_type = "Enrollee"

    def print_info(self):
        super().print_info()
        print('Faculty: ', self.faculty)


class Student(Enrollee):
    def __init__(
            self,
            full_name: str = None,
            date_of_birth: str = None,
            faculty: str = None,
            course: str = None):
        super().__init__(full_name, date_of_birth, faculty)
        self.course = course if course else "Not given"
        self.person_type = "Student"

    def print_info(self):
        super().print_info()
        print('Course: ', self.course)


class Teacher(Enrollee):

    def __init__(
            self,
            full_name: str = None,
            date_of_birth: str = None,
            faculty: str = None,
            position: str = None,
            experience: float = None):
        super().__init__(full_name, date_of_birth, faculty)
        self.position = position if position else "Not given"
        self.exp = experience if experience else "Not given"
        self.person_type = "Teacher"

    def print_info(self):
        super().print_info()
        print('Position: ', self.position)
        print('Experience: ', self.exp)


if __name__ == "__main__":
    enrollee1 = Enrollee("First Enrollee", "01/06/2002", "Finance")
    enrollee2 = Enrollee("Second Enrollee", "25/02/1999", "Economics")
    student1 = Student("First Student", "13/07/2000", "Linguistics", "FFL")
    teacher1 = Teacher("First Teacher", "25/10/1983", "Maths", "Professor", 20.4)
    library = LibrarySingleton()
    library.print_all_records()
    library.print_records_by_age_range(20, 25)
