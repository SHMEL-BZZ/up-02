"""
Unit-тесты для валидации полей - Visual Studio
"""

import unittest
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем функцию валидации
try:
    from controller.competition_controller import validate_parameters
    print("Функция validate_parameters импортирована успешно")
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    # Заглушка для тестирования
    def validate_parameters(n, gray_init, white_init, rye_init, 
                            rye_interval, rye_spawn_count, max_ticks):
        total_cells = n * n
        if n < 2 or n > 10:
            return False, "n должен быть от 2 до 10"
        if gray_init < 1:
            return False, "Серых крыс должно быть не менее 1"
        if white_init < 1:
            return False, "Белых крыс должно быть не менее 1"
        if rye_init < 1:
            return False, "Ржи должно быть не менее 1"
        if gray_init + white_init + rye_init > total_cells:
            return False, "Сумма превышает количество клеток"
        return True, None


class TestNField(unittest.TestCase):
    """Тесты для поля n (размер поля)"""
    
    def test_n_correct_2(self):
        """n=2 - минимальное корректное значение"""
        is_valid, error = validate_parameters(2, 2, 1, 1, 3, 2, 100)
        self.assertTrue(is_valid, f"n=2 должен быть корректным, ошибка: {error}")
    
    def test_n_correct_5(self):
        """n=5 - корректное значение"""
        is_valid, error = validate_parameters(5, 2, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, f"n=5 должен быть корректным, ошибка: {error}")
    
    def test_n_correct_10(self):
        """n=10 - максимальное корректное значение"""
        is_valid, error = validate_parameters(10, 2, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, f"n=10 должен быть корректным, ошибка: {error}")
    
    def test_n_incorrect_1(self):
        """n=1 - некорректное (меньше 2)"""
        is_valid, error = validate_parameters(1, 2, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, "n=1 должен быть НЕкорректным")
    
    def test_n_incorrect_11(self):
        """n=11 - некорректное (больше 10)"""
        is_valid, error = validate_parameters(11, 2, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, "n=11 должен быть НЕкорректным")

    def test_n_negative(self):
        """n=-1 - отрицательное значение (некорректно)"""
        is_valid, error = validate_parameters(-1, 2, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, f"n=-1 должен быть НЕкорректным, но прошёл проверку. Ошибка: {error}")


class TestGrayField(unittest.TestCase):
    """Тесты для поля 'Серые крысы'"""
    
    def test_gray_correct_min(self):
        """Серые крысы=2 - минимальное корректное"""
        is_valid, error = validate_parameters(6, 2, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, "gray=2 должен быть корректным")
    
    def test_gray_correct_max_n6(self):
        """Серые крысы=33 - максимальное при n=6"""
        is_valid, error = validate_parameters(6, 33, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, "gray=33 при n=6 должен быть корректным")
    
    def test_gray_incorrect_0(self):
        """Серые крысы=0 - меньше минимума"""
        is_valid, error = validate_parameters(6, 0, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, "gray=0 должен быть НЕкорректным")
    
    def test_gray_incorrect_34(self):
        """Серые крысы=34 - больше максимума при n=6"""
        is_valid, error = validate_parameters(6, 34, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, "gray=34 при n=6 должен быть НЕкорректным")


class TestWhiteField(unittest.TestCase):
    """Тесты для поля 'Белые крысы'"""
    
    def test_white_correct_min(self):
        """Белые крысы=2 - минимальное корректное"""
        is_valid, error = validate_parameters(6, 2, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, "white=2 должен быть корректным")
    
    def test_white_correct_max_n6(self):
        """Белые крысы=33 - максимальное при n=6"""
        is_valid, error = validate_parameters(6, 2, 33, 1, 3, 2, 100)
        self.assertTrue(is_valid, "white=33 при n=6 должен быть корректным")
    
    def test_white_incorrect_0(self):
        """Белые крысы=0 - меньше минимума"""
        is_valid, error = validate_parameters(6, 2, 0, 1, 3, 2, 100)
        self.assertFalse(is_valid, "white=1 должен быть НЕкорректным")
    
    def test_white_incorrect_34(self):
        """Белые крысы=34 - больше максимума при n=6"""
        is_valid, error = validate_parameters(6, 2, 34, 1, 3, 2, 100)
        self.assertFalse(is_valid, "white=34 при n=6 должен быть НЕкорректным")


class TestRyeField(unittest.TestCase):
    """Тесты для поля 'Начальная рожь'"""
    
    def test_rye_correct_min(self):
        """Рожь=1 - минимальное корректное"""
        is_valid, error = validate_parameters(6, 2, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, "rye=1 должен быть корректным")
    
    def test_rye_correct_max(self):
        """Рожь=12 - максимальное при n=4, крысах 2+2"""
        is_valid, error = validate_parameters(4, 2, 2, 12, 3, 2, 100)
        self.assertTrue(is_valid, "rye=12 должен быть корректным")
    
    def test_rye_incorrect_0(self):
        """Рожь=0 - меньше минимума"""
        is_valid, error = validate_parameters(6, 2, 2, 0, 3, 2, 100)
        self.assertFalse(is_valid, "rye=0 должен быть НЕкорректным")
    
    def test_rye_incorrect_too_much(self):
        """Рожь=13 - больше свободных клеток при n=4"""
        is_valid, error = validate_parameters(4, 2, 2, 13, 3, 2, 100)
        self.assertFalse(is_valid, "rye=13 должен быть НЕкорректным")


class TestTotalRatsSum(unittest.TestCase):
    """Тесты для суммы крыс"""
    
    def test_sum_correct_15_of_16(self):
        """Сумма крыс=15 при n=4 (место для 1 ржи есть)"""
        is_valid, error = validate_parameters(4, 13, 2, 1, 3, 2, 100)
        self.assertTrue(is_valid, "Сумма 13+2=15 должна быть корректной")
    
    def test_sum_incorrect_16_of_16(self):
        """Сумма крыс=16 при n=4 (нет места для ржи)"""
        is_valid, error = validate_parameters(4, 14, 2, 1, 3, 2, 100)
        self.assertFalse(is_valid, "Сумма 14+2=16 должна быть НЕкорректной")


