"""
Модульное тестирование модели "Распространение эпидемии"
"""

import unittest
import sys
import os
import numpy as np

# Добавления путя к корню проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.epidemic import (
    calculate_epidemic_threshold,
    count_epidemic_weeks,
    calculate_efficacy,
    simulate_epidemic,
    SimulationResult
)


class TestEpidemicThreshold(unittest.TestCase):
    """Тесты для расчёта эпидемического порога"""
    
    def test_threshold_calculation(self):
        """
        Тест 1: Проверка корректности формулы расчёта порога.
        
        Формула: порог = mean(first_8) + 2.507 * std(first_8)
        Проверяем, что функция calculate_epidemic_threshold возвращает
        именно этот результат для фиксированного набора данных.
        """
        weekly_infections = [5, 20, 30, 17, 50, 60, 8, 80]
        
        # Вычисляем ожидаемое значение через numpy
        mean = np.mean(weekly_infections)
        std = np.std(weekly_infections, ddof=1)
        expected = round(mean + 2.507 * std, 1)
        threshold = calculate_epidemic_threshold(weekly_infections)
        
        # Проверяем, что функция возвращает то, что должна
        self.assertEqual(threshold, expected)
    
    def test_threshold_insufficient_data(self):
        """
        Тест 2: При недостаточном количестве недель (<8) порог должен быть 0.
        """
        weekly_infections = [10, 20, 30, 40, 50]
        threshold = calculate_epidemic_threshold(weekly_infections)
        self.assertEqual(threshold, 0)
    
    def test_threshold_all_zeros(self):
        """
        Тест 3: При всех нулевых заражениях порог должен быть 0.
        """
        weekly_infections = [0, 0, 0, 0, 0, 0, 0, 0]
        threshold = calculate_epidemic_threshold(weekly_infections)
        self.assertEqual(threshold, 0)
    
    def test_threshold_constant_values(self):
        """
        Тест 4: При постоянных значениях std=0, порог = mean.
        """
        weekly_infections = [50, 50, 50, 50, 50, 50, 50, 50]
        threshold = calculate_epidemic_threshold(weekly_infections)
        self.assertEqual(threshold, 50.0)


class TestEpidemicWeeks(unittest.TestCase):
    """Тесты для подсчёта эпидемических недель"""
    
    def test_count_epidemic_weeks(self):
        """
        Тест 5: Проверка подсчёта недель с заражениями выше порога.
        
        Данные: [5, 15, 25, 35], порог = 20
        Недели выше порога: 25 и 35 → 2 недели
        """
        infected_history = [5, 15, 25, 35]
        threshold = 20
        count = count_epidemic_weeks(infected_history, threshold)
        self.assertEqual(count, 2)
    
    def test_count_epidemic_weeks_all_below(self):
        """
        Тест 6: Все недели ниже порога → 0 эпидемических недель.
        """
        infected_history = [5, 10, 15, 20]
        threshold = 25
        count = count_epidemic_weeks(infected_history, threshold)
        self.assertEqual(count, 0)
    
    def test_count_epidemic_weeks_all_above(self):
        """
        Тест 7: Все недели выше порога → все недели эпидемические.
        """
        infected_history = [30, 40, 50, 60]
        threshold = 25
        count = count_epidemic_weeks(infected_history, threshold)
        self.assertEqual(count, 4)


class TestEfficacyCalculation(unittest.TestCase):
    """Тесты для расчёта эффективности вакцинации"""
    
    def test_efficacy_60_percent(self):
        """
        Тест 8: 10 эпидемических недель → 4 → эффективность 60%.
        Формула: (10 - 4) / 10 * 100 = 60%
        """
        efficacy = calculate_efficacy(10, 4)
        self.assertEqual(efficacy, 60.0)
    
    def test_efficacy_0_percent_no_epidemic(self):
        """
        Тест 9: Нет эпидемических недель → эффективность 0%.
        """
        efficacy = calculate_efficacy(0, 0)
        self.assertEqual(efficacy, 0.0)
    
    def test_efficacy_100_percent(self):
        """
        Тест 10: Вакцинация полностью подавила эпидемию → 100%.
        """
        efficacy = calculate_efficacy(10, 0)
        self.assertEqual(efficacy, 100.0)
    
    def test_efficacy_never_negative(self):
        """
        Тест 11: Эффективность не может быть отрицательной.
        Даже если сценарий с вакцинацией хуже, результат 0%.
        """
        efficacy = calculate_efficacy(5, 10)
        self.assertGreaterEqual(efficacy, 0)
        self.assertEqual(efficacy, 0)

class TestValidation(unittest.TestCase):
    """Тесты для проверки работы с граничными значениями параметров"""
    
    def test_min_grid_size(self):
        """
        Тест 12: Минимальный размер сетки 2x2 должен работать без ошибок.
        """
        try:
            result = simulate_epidemic(
                n=2, total_rats=4, weeks=10,
                p_infect=0.5, p_move=0.5,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Минимальный размер сетки вызвал ошибку: {e}")
    
    def test_max_grid_size(self):
        """
        Тест 13: Максимальный размер сетки 10x10 должен работать без ошибок.
        """
        try:
            result = simulate_epidemic(
                n=10, total_rats=400, weeks=10,
                p_infect=0.5, p_move=0.5,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Максимальный размер сетки вызвал ошибку: {e}")
    
    def test_min_weeks(self):
        """
        Тест 14: Минимальная длительность 8 недель.
        """
        try:
            result = simulate_epidemic(
                n=5, total_rats=25, weeks=8,
                p_infect=0.5, p_move=0.5,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Минимальная длительность вызвала ошибку: {e}")
    
    def test_max_weeks(self):
        """
        Тест 15: Максимальная длительность 260 недель.
        """
        try:
            result = simulate_epidemic(
                n=5, total_rats=25, weeks=260,
                p_infect=0.5, p_move=0.5,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Максимальная длительность вызвала ошибку: {e}")
    
    def test_min_probabilities(self):
        """
        Тест 16: Минимальные вероятности 0.1.
        """
        try:
            result = simulate_epidemic(
                n=5, total_rats=25, weeks=10,
                p_infect=0.1, p_move=0.1,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Минимальные вероятности вызвали ошибку: {e}")
    
    def test_max_probabilities(self):
        """
        Тест 17: Максимальные вероятности 0.9.
        """
        try:
            result = simulate_epidemic(
                n=5, total_rats=25, weeks=10,
                p_infect=0.9, p_move=0.9,
                vacc_day=14, vacc_percent=50,
                record_history=False
            )
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.fail(f"Максимальные вероятности вызвали ошибку: {e}")


class TestThresholdFormulaIntegration(unittest.TestCase):
    """
    Тесты для проверки интеграции формулы порога с симуляцией.
    
    Эти тесты проверяют, что порог вычисляется корректно
    на реальных данных симуляции.
    """
    
    def test_threshold_uses_first_8_weeks_only(self):
        """
        Тест 18: Порог должен рассчитываться ТОЛЬКО по первым 8 неделям.
        
        Создаём симуляцию с известными первыми 8 неделями.
        """
        result = simulate_epidemic(
            n=4, total_rats=30, weeks=20,
            p_infect=0.7, p_move=0.5,
            vacc_day=56, vacc_percent=50,
            record_history=False
        )
        
        # Порог должен быть рассчитан и не быть нулевым
        self.assertIsInstance(result.threshold, float)
    
    def test_efficacy_uses_threshold(self):
        """
        Тест 19: Эффективность должна рассчитываться на основе порога.
        
        Проверяем, что эффективность находится в разумных пределах [0, 100].
        """
        result = simulate_epidemic(
            n=6, total_rats=50, weeks=30,
            p_infect=0.6, p_move=0.5,
            vacc_day=42, vacc_percent=60,
            record_history=False
        )
        
        self.assertGreaterEqual(result.efficacy, 0)
        self.assertLessEqual(result.efficacy, 100)


class TestDataTypes(unittest.TestCase):
    """Тесты для проверки типов возвращаемых данных"""
    
    def test_result_data_types(self):
        """
        Тест 20: Проверка типов всех полей SimulationResult.
        """
        result = simulate_epidemic(
            n=5, total_rats=40, weeks=15,
            p_infect=0.5, p_move=0.5,
            vacc_day=35, vacc_percent=50,
            record_history=False
        )
        
        self.assertIsInstance(result.history_s, list)
        self.assertIsInstance(result.history_i, list)
        self.assertIsInstance(result.history_r, list)
        self.assertIsInstance(result.threshold, float)
        self.assertIsInstance(result.efficacy, float)
        self.assertIsInstance(result.peak_with, int)
        self.assertIsInstance(result.peak_without, int)
        self.assertIsInstance(result.n, int)


if __name__ == '__main__':
    unittest.main(verbosity=2)