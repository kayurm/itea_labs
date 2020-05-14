"""Kateryna Yurmanovych
     lesson 3
     Homework

Создать класс
комплексного числа и реализовать для него арифметические
операции."""
import cmath


class ComplexNum:
    def __init__(self, num1: int, num2: int):
        self._complex_num = complex(num1, num2)

    def get_real_part(self):
        return self._complex_num.real

    def get_imag_part(self):
        return self._complex_num.imag

    def __add__(self, other):
        return self._complex_num + other._complex_num

    def __sub__(self, other):
        return self._complex_num - other._complex_num

    def __mul__(self, other):
        return self._complex_num * other._complex_num

    def __truediv__(self, other):
        return self._complex_num / other._complex_num


if __name__ == "__main__":
    my_complex_num1 = ComplexNum(1, 2)
    print(f"Real and imaginary parts of first num:", my_complex_num1.get_real_part(), my_complex_num1.get_imag_part())
    my_complex_num2 = ComplexNum(3, 4)
    print(f"Real and imaginary parts of second num:", my_complex_num2.get_real_part(), my_complex_num2.get_imag_part())
    print("Below are the arithmetic operations sum/ sub/ mul/ div respectively:")
    print(my_complex_num1.__add__(my_complex_num2))
    print(my_complex_num1.__sub__(my_complex_num2))
    print(my_complex_num1.__mul__(my_complex_num2))
    print(my_complex_num1.__truediv__(my_complex_num2))


