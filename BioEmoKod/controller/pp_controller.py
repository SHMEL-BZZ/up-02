
"""
Модуль с расчетной логикой модели "Хищник-жертва" (Лотки-Вольтерры)
Для независимого тестирования и использования в других файлах
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SimulationResult:
    """Результат симуляции модели хищник-жертва."""
    time: List[float]          # массив времени
    prey: List[float]          # численность жертв (кролики)
    predators: List[float]     # численность хищников (лисы)
    equilibrium_prey: float    # равновесная численность жертв
    equilibrium_predator: float # равновесная численность хищников
    period: float              # период колебаний
    stability_type: str        # тип устойчивости
    avg_prey: float            # средняя численность жертв
    avg_predator: float        # средняя численность хищников


def calculate_equilibrium(alpha: float, c: float, beta: float, d: float) -> tuple:
    """
    Расчет равновесных значений численности.
    
    Параметры:
        alpha: скорость размножения жертв
        c: эффективность охоты хищника
        beta: скорость гибели хищников
        d: вклад съеденной жертвы в размножение хищника
    
    Возвращает:
        (equilibrium_prey, equilibrium_predator)
    """
    prey_eq = beta / d if d > 0 else 0
    predator_eq = alpha / c if c > 0 else 0
    return prey_eq, predator_eq


def calculate_period(alpha: float, beta: float) -> float:
    """
    Расчет периода малых колебаний.
    
    Параметры:
        alpha: скорость размножения жертв
        beta: скорость гибели хищников
    
    Возвращает:
        период колебаний
    """
    return 2 * np.pi / np.sqrt(alpha * beta) if alpha * beta > 0 else 0


def calculate_dx_dt(prey: float, predators: float, alpha: float, c: float) -> float:
    """
    Расчет скорости изменения численности жертв.
    
    Параметры:
        prey: текущая численность жертв
        predators: текущая численность хищников
        alpha: скорость размножения жертв
        c: эффективность охоты хищника
    
    Возвращает:
        dx/dt
    """
    return alpha * prey - c * prey * predators


def calculate_dy_dt(prey: float, predators: float, d: float, beta: float) -> float:
    """
    Расчет скорости изменения численности хищников.
    
    Параметры:
        prey: текущая численность жертв
        predators: текущая численность хищников
        d: вклад съеденной жертвы в размножение хищника
        beta: скорость гибели хищников
    
    Возвращает:
        dy/dt
    """
    return d * prey * predators - beta * predators


def euler_step(prey: float, predators: float, dt: float, 
               alpha: float, c: float, d: float, beta: float) -> tuple:
    """
    Один шаг метода Эйлера для системы Лотки-Вольтерры.
    
    Параметры:
        prey: текущая численность жертв
        predators: текущая численность хищников
        dt: шаг по времени
        alpha, c, d, beta: параметры модели
    
    Возвращает:
        (prey_next, predators_next) - численности на следующем шаге
    """
    dx_dt = calculate_dx_dt(prey, predators, alpha, c)
    dy_dt = calculate_dy_dt(prey, predators, d, beta)
    
    prey_next = prey + dx_dt * dt
    predators_next = predators + dy_dt * dt
    
    # Биологическая корректность (неотрицательные значения)
    prey_next = max(prey_next, 0)
    predators_next = max(predators_next, 0)
    
    return prey_next, predators_next


def simulate_lotka_volterra_core(
    x0: float,
    y0: float,
    alpha: float,
    c: float,
    beta: float,
    d: float,
    T: float,
    N: int
) -> tuple:
    """
    Ядро численного интегрирования модели Лотки-Вольтерры.
    
    Параметры:
        x0, y0: начальные численности
        alpha, c, beta, d: параметры модели
        T: длительность моделирования
        N: количество шагов
    
    Возвращает:
        (time_array, prey_array, predators_array)
    """
    dt = T / N
    
    # Инициализация массивов
    time = np.zeros(N + 1)
    prey = np.zeros(N + 1)
    predators = np.zeros(N + 1)
    
    # Начальные условия
    time[0] = 0
    prey[0] = x0
    predators[0] = y0
    
    # Численное интегрирование
    for i in range(N):
        prey[i + 1], predators[i + 1] = euler_step(
            prey[i], predators[i], dt, alpha, c, d, beta
        )
        time[i + 1] = time[i] + dt
    
    return time, prey, predators


def calculate_averages(prey_array: np.ndarray, predators_array: np.ndarray) -> tuple:
    """
    Расчет средних значений численности.
    
    Параметры:
        prey_array: массив численности жертв
        predators_array: массив численности хищников
    
    Возвращает:
        (avg_prey, avg_predator)
    """
    return float(np.mean(prey_array)), float(np.mean(predators_array))


def check_realistic(prey_array: np.ndarray, predators_array: np.ndarray,
                   max_prey: float = 500, max_predators: float = 200) -> bool:
    """
    Проверка биологической реалистичности результатов.
    
    Параметры:
        prey_array: массив численности жертв
        predators_array: массив численности хищников
        max_prey: максимальное допустимое значение жертв
        max_predators: максимальное допустимое значение хищников
    
    Возвращает:
        True если результат реалистичен, иначе False
    """
    return (max(prey_array) < max_prey and 
            max(predators_array) < max_predators and
            min(prey_array) >= 0 and
            min(predators_array) >= 0)


def simulate_lotka_volterra(
    x0: float = 50.0,
    y0: float = 10.0,
    alpha: float = 0.8,
    c: float = 0.03,
    beta: float = 0.6,
    d: float = 0.02,
    T: float = 50.0,
    N: int = 1000,
    seed: Optional[int] = None
) -> SimulationResult:
    """
    Основная функция симуляции (использует расчетное ядро).
    
    Параметры:
        x0, y0: начальные численности
        alpha, c, beta, d: параметры модели
        T: длительность моделирования
        N: количество шагов
        seed: зерно для воспроизводимости
    
    Возвращает:
        SimulationResult с историей популяций и аналитическими данными
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Численное интегрирование
    time, prey, predators = simulate_lotka_volterra_core(
        x0, y0, alpha, c, beta, d, T, N
    )
    
    # Расчет равновесных значений
    equilibrium_prey, equilibrium_predator = calculate_equilibrium(alpha, c, beta, d)
    
    # Расчет периода
    period = calculate_period(alpha, beta)
    
    # Тип устойчивости (для классической модели - центр)
    stability_type = "Центр (консервативные колебания)"
    
    # Средние значения
    avg_prey, avg_predator = calculate_averages(prey, predators)
    
    return SimulationResult(
        time=time.tolist(),
        prey=prey.tolist(),
        predators=predators.tolist(),
        equilibrium_prey=equilibrium_prey,
        equilibrium_predator=equilibrium_predator,
        period=period,
        stability_type=stability_type,
        avg_prey=avg_prey,
        avg_predator=avg_predator
    )


