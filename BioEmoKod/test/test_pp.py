"""
Unit-тесты для модели "Хищник-жертва" (Лотки-Вольтерры)
Полное покрытие всех функций и методов
"""

import unittest
import numpy as np
from model.pp_model import *

class TestEquilibriumCalculations(unittest.TestCase):
    """Тесты для расчета равновесных значений"""
    
    def test_normal_case(self):
        """Нормальный случай с положительными параметрами"""
        prey_eq, pred_eq = calculate_equilibrium(alpha=0.8, c=0.03, beta=0.6, d=0.02)
        self.assertAlmostEqual(prey_eq, 30.0)  # beta/d = 0.6/0.02
        self.assertAlmostEqual(pred_eq, 26.666666666666668)  # alpha/c = 0.8/0.03
    
    def test_zero_division_protection(self):
        """Защита от деления на ноль"""
        prey_eq, pred_eq = calculate_equilibrium(alpha=0.8, c=0, beta=0.6, d=0)
        self.assertEqual(prey_eq, 0)
        self.assertEqual(pred_eq, float('inf') if 0.8/0 else 0)
    
    def test_zero_d(self):
        """d равно нулю"""
        prey_eq, pred_eq = calculate_equilibrium(alpha=0.8, c=0.03, beta=0.6, d=0)
        self.assertEqual(prey_eq, 0)
        self.assertAlmostEqual(pred_eq, 26.666666666666668)
    
    def test_zero_c(self):
        """c равно нулю"""
        prey_eq, pred_eq = calculate_equilibrium(alpha=0.8, c=0, beta=0.6, d=0.02)
        self.assertAlmostEqual(prey_eq, 30.0)
        self.assertEqual(pred_eq, float('inf'))

class TestPeriodCalculation(unittest.TestCase):
    """Тесты для расчета периода колебаний"""
    
    def test_normal_case(self):
        """Нормальный случай с положительными параметрами"""
        period = calculate_period(alpha=0.8, beta=0.6)
        expected = 2 * np.pi / np.sqrt(0.8 * 0.6)
        self.assertAlmostEqual(period, expected)
    
    def test_zero_product(self):
        """Произведение параметров равно нулю"""
        period = calculate_period(alpha=0, beta=0.6)
        self.assertEqual(period, 0)
        
        period = calculate_period(alpha=0.8, beta=0)
        self.assertEqual(period, 0)
    
    def test_negative_product(self):
        """Отрицательное произведение"""
        period = calculate_period(alpha=-0.8, beta=0.6)
        self.assertEqual(period, 0)

class TestDifferentialEquations(unittest.TestCase):
    """Тесты для дифференциальных уравнений"""
    
    def test_prey_growth_without_predators(self):
        """Рост жертв при отсутствии хищников"""
        dx_dt = calculate_dx_dt(prey=50, predators=0, alpha=0.8, c=0.03)
        self.assertEqual(dx_dt, 40.0)  # 0.8 * 50
    
    def test_prey_decline_with_many_predators(self):
        """Снижение численности жертв при большом числе хищников"""
        dx_dt = calculate_dx_dt(prey=50, predators=100, alpha=0.8, c=0.03)
        self.assertLess(dx_dt, 0)  # Должно быть отрицательным
    
    def test_predator_growth_with_plenty_prey(self):
        """Рост хищников при обилии жертв"""
        dy_dt = calculate_dy_dt(prey=100, predators=10, d=0.02, beta=0.6)
        self.assertGreater(dy_dt, 0)  # 0.02*100*10 - 0.6*10 = 20 - 6 = 14
    
    def test_predator_decline_with_few_prey(self):
        """Снижение численности хищников при недостатке жертв"""
        dy_dt = calculate_dy_dt(prey=10, predators=10, d=0.02, beta=0.6)
        self.assertLess(dy_dt, 0)  # 0.02*10*10 - 0.6*10 = 2 - 6 = -4
    
    def test_zero_populations(self):
        """Нулевые популяции"""
        dx_dt = calculate_dx_dt(prey=0, predators=0, alpha=0.8, c=0.03)
        self.assertEqual(dx_dt, 0)
        
        dy_dt = calculate_dy_dt(prey=0, predators=0, d=0.02, beta=0.6)
        self.assertEqual(dy_dt, 0)

class TestEulerStep(unittest.TestCase):
    """Тесты для шага метода Эйлера"""
    
    def test_normal_step(self):
        """Нормальный шаг интегрирования"""
        prey_next, pred_next = euler_step(


        prey=50, predators=10, dt=0.05,
            alpha=0.8, c=0.03, d=0.02, beta=0.6
        )
        # dx_dt = 0.8*50 - 0.03*50*10 = 40 - 15 = 25
        # prey_next = 50 + 25*0.05 = 51.25
        # dy_dt = 0.02*50*10 - 0.6*10 = 10 - 6 = 4
        # pred_next = 10 + 4*0.05 = 10.2
        self.assertAlmostEqual(prey_next, 51.25)
        self.assertAlmostEqual(pred_next, 10.2)
    
    def test_non_negative_constraint(self):
        """Проверка ограничения на неотрицательные значения"""
        # Ситуация, когда популяция может стать отрицательной
        prey_next, pred_next = euler_step(
            prey=1, predators=100, dt=1.0,
            alpha=0.8, c=0.03, d=0.02, beta=0.6
        )
        self.assertGreaterEqual(prey_next, 0)
        self.assertGreaterEqual(pred_next, 0)
    
    def test_zero_step(self):
        """Нулевой шаг по времени"""
        prey_next, pred_next = euler_step(
            prey=50, predators=10, dt=0,
            alpha=0.8, c=0.03, d=0.02, beta=0.6
        )
        self.assertEqual(prey_next, 50)
        self.assertEqual(pred_next, 10)

class TestSimulationCore(unittest.TestCase):
    """Тесты для ядра симуляции"""
    
    def test_output_shapes(self):
        """Проверка размеров выходных массивов"""
        time, prey, predators = simulate_lotka_volterra_core(
            x0=50, y0=10, alpha=0.8, c=0.03,
            beta=0.6, d=0.02, T=50, N=1000
        )
        self.assertEqual(len(time), 1001)
        self.assertEqual(len(prey), 1001)
        self.assertEqual(len(predators), 1001)
    
    def test_initial_conditions(self):
        """Проверка начальных условий"""
        time, prey, predators = simulate_lotka_volterra_core(
            x0=50, y0=10, alpha=0.8, c=0.03,
            beta=0.6, d=0.02, T=50, N=1000
        )
        self.assertEqual(time[0], 0)
        self.assertEqual(prey[0], 50)
        self.assertEqual(predators[0], 10)
    
    def test_time_array(self):
        """Проверка правильности временной сетки"""
        N = 100
        T = 10
        time, _, _ = simulate_lotka_volterra_core(
            x0=50, y0=10, alpha=0.8, c=0.03,
            beta=0.6, d=0.02, T=T, N=N
        )
        expected_dt = T / N
        for i in range(len(time) - 1):
            self.assertAlmostEqual(time[i+1] - time[i], expected_dt)
        self.assertAlmostEqual(time[-1], T)
    
    def test_zero_initial_populations(self):
        """Нулевые начальные популяции"""
        time, prey, predators = simulate_lotka_volterra_core(
            x0=0, y0=0, alpha=0.8, c=0.03,
            beta=0.6, d=0.02, T=50, N=1000
        )
        # Все значения должны остаться нулевыми
        self.assertTrue(np.all(prey == 0))
        self.assertTrue(np.all(predators == 0))
    
    def test_only_prey_initial(self):
        """Только жертвы в начальный момент"""
        time, prey, predators = simulate_lotka_volterra_core(
            x0=50, y0=0, alpha=0.8, c=0.03,
            beta=0.6, d=0.02, T=10, N=100
        )
        # Жертвы должны расти экспоненциально
        self.assertGreater(prey[-1], prey[0])
        # Хищники должны остаться нулевыми (нет пищи для роста)
        self.assertTrue(np.all(predators == 0))

class TestAverages(unittest.TestCase):
    """Тесты для расчета средних значений"""
    
    def test_normal_averages(self):
        """Нормальный расчет средних"""
        prey_array = np.array([10, 20, 30, 40, 50])
        pred_array = np.array([5, 10, 15, 20, 25])
        
        avg_prey, avg_pred = calculate_averages(prey_array, pred_array)
        
        self.assertEqual(avg_prey, 30.0)
        self.assertEqual(avg_pred, 15.0)
    
    def test_single_element(self):
        """Массив из одного элемента"""
        prey_array = np.array([100])
        pred_array = np.array([50])
        
        avg_prey, avg_pred = calculate_averages(prey_array, pred_array)
        
        self.assertEqual(avg_prey, 100.0)
        self.assertEqual(avg_pred, 50.0)
    
    def test_empty_array(self):
        """Пустой массив"""
        prey_array = np.array([])
        pred_array = np.array([])
        
        # Должен вернуть nan (среднее от пустого массива)
        avg_prey, avg_pred = calculate_averages(prey_array, pred_array)
        self.assertTrue(np.isnan(avg_prey))
        self.assertTrue(np.isnan(avg_pred))

class TestRealisticCheck(unittest.TestCase):
    """Тесты для проверки биологической реалистичности"""
    
    def test_realistic_case(self):
        """Реалистичный случай"""
        prey = np.array([10, 50, 100, 200, 300])
        predators = np.array([5, 20, 50, 100, 150])
        
        self.assertTrue(check_realistic(prey, predators, max_prey=500, max_predators=200))
    
    def test_exceeds_max_prey(self):
        """Превышение максимальной численности жертв"""
        prey = np.array([10, 600, 100])
        predators = np.array([5, 50, 100])
        
        self.assertFalse(check_realistic(prey, predators, max_prey=500, max_predators=200))
    
    def test_exceeds_max_predators(self):
        """Превышение максимальной численности хищников"""
        prey = np.array([10, 100, 200])
        predators = np.array([5, 250, 100])
        
        self.assertFalse(check_realistic(prey, predators, max_prey=500, max_predators=200))
    
    def test_negative_values(self):
        """Отрицательные значения"""
        prey = np.array([10, -5, 100])
        predators = np.array([5, 10, 50])
        
        self.assertFalse(check_realistic(prey, predators))
    
    def test_zero_values_allowed(self):
        """Нулевые значения допустимы"""
        prey = np.array([0, 50, 100])
        predators = np.array([0, 10, 20])
        
        self.assertTrue(check_realistic(prey, predators))

class TestFullSimulation(unittest.TestCase):
    """Тесты для полной симуляции"""
    
    def test_return_type(self):
        """Проверка типа возвращаемого значения"""
        result = simulate_lotka_volterra()
        self.assertIsInstance(result, SimulationResult)
    
    def test_default_parameters(self):
        """Тест с параметрами по умолчанию"""
        result = simulate_lotka_volterra()
        
        self.assertEqual(len(result.time), 1001)
        self.assertEqual(len(result.prey), 1001)
        self.assertEqual(len(result.predators), 1001)
        self.assertEqual(result.time[0], 0)
        self.assertEqual(result.time[-1], 50)
        self.assertEqual(result.prey[0], 50)
        self.assertEqual(result.predators[0], 10)
    
    def test_equilibrium_calculation(self):
        """Проверка расчета равновесных значений"""
        result = simulate_lotka_volterra(
            alpha=0.8, c=0.03, beta=0.6, d=0.02
        )
        self.assertAlmostEqual(result.equilibrium_prey, 30.0)
        self.assertAlmostEqual(result.equilibrium_predator, 26.666666666666668)
    
    def test_period_calculation(self):
        """Проверка расчета периода"""
        result = simulate_lotka_volterra(alpha=0.8, beta=0.6)
        expected_period = 2 * np.pi / np.sqrt(0.8 * 0.6)
        self.assertAlmostEqual(result.period, expected_period)
    
    def test_stability_type(self):
        """Проверка типа устойчивости"""
        result = simulate_lotka_volterra()
        self.assertEqual(result.stability_type, "Центр (консервативные колебания)")
    
    def test_seed_reproducibility(self):
        """Проверка воспроизводимости с одинаковым seed"""
        result1 = simulate_lotka_volterra(seed=42)
        result2 = simulate_lotka_volterra(seed=42)
        
        self.assertEqual(result1.prey, result2.prey)
        self.assertEqual(result1.predators, result2.predators)
    
    def test_different_seeds(self):
        """Разные seed дают разные результаты (если есть случайность)"""
        result1 = simulate_lotka_volterra(seed=42)
        result2 = simulate_lotka_volterra(seed=43)
        
        # В текущей реализации нет случайности, поэтому результаты должны совпадать
        # Но если добавите шум, тест нужно будет изменить
        self.assertEqual(result1.prey, result2.prey)
    
    def test_custom_parameters(self):
        """Тест с пользовательскими параметрами"""
        result = simulate_lotka_volterra(
            x0=100, y0=20, alpha=0.5, c=0.02,
            beta=0.4, d=0.01, T=100, N=500
        )
        
        self.assertEqual(result.prey[0], 100)
        self.assertEqual(result.predators[0], 20)
        self.assertEqual(len(result.time), 501)
        self.assertAlmostEqual(result.time[-1], 100)
    
    def test_simulation_stability(self):
        """Проверка стабильности симуляции (неотрицательные значения)"""
        result = simulate_lotka_volterra(T=100, N=10000)
        
        self.assertTrue(all(p >= 0 for p in result.prey))
        self.assertTrue(all(p >= 0 for p in result.predators))
    
    def test_average_values(self):
        """Проверка средних значений"""
        result = simulate_lotka_volterra(T=100, N=10000)
        
        self.assertIsInstance(result.avg_prey, float)
        self.assertIsInstance(result.avg_predator, float)
        self.assertGreaterEqual(result.avg_prey, 0)
        self.assertGreaterEqual(result.avg_predator, 0)

class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""
    
    def test_very_large_time(self):
        """Очень большое время симуляции"""
        result = simulate_lotka_volterra(T=10000, N=100000)
        
        # Проверяем, что значения не стали бесконечными
        self.assertTrue(all(np.isfinite(p) for p in result.prey))
        self.assertTrue(all(np.isfinite(p) for p in result.predators))
    
    def test_very_small_step(self):
        """Очень маленький шаг интегрирования"""
        result = simulate_lotka_volterra(T=10, N=100000)
        
        self.assertEqual(len(result.time), 100001)
    
    def test_extreme_parameters(self):
        """Экстремальные значения параметров"""
        result = simulate_lotka_volterra(
            alpha=10.0, c=0.001, beta=10.0, d=0.001
        )
        
        # Проверяем, что симуляция не падает
        self.assertIsNotNone(result)
    
    def test_negative_parameters(self):
        """Отрицательные параметры (может привести к нестабильности)"""
        # Симуляция должна завершиться без ошибок
        result = simulate_lotka_volterra(
            alpha=-0.8, c=0.03, beta=-0.6, d=0.02
        )
        self.assertIsNotNone(result)

if __name__ == '__main__':
    # Настройка для запуска тестов с подробным выводом
    unittest.main(verbosity=2)
