"""
Модель динамики системы "Хищник-жертва" (Лотки-Вольтерры).
Вариант ___ (впишите свой вариант)
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional
import io
import base64


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


def simulate_lotka_volterra(
    x0: float = 50.0,          # начальная численность жертв
    y0: float = 10.0,          # начальная численность хищников
    alpha: float = 0.8,        # скорость размножения жертв
    c: float = 0.03,           # эффективность охоты хищника
    beta: float = 0.6,         # скорость гибели хищников
    d: float = 0.02,           # вклад съеденной жертвы в размножение хищника
    T: float = 50.0,           # длительность моделирования (лет)
    N: int = 1000,             # количество шагов интегрирования
    seed: Optional[int] = None
) -> SimulationResult:
    """
    Один прогон модели Лотки-Вольтерры.
    
    Параметры:
        x0: начальная численность жертв (10-100)
        y0: начальная численность хищников (1-50)
        alpha: скорость размножения жертв без хищников (0.4-1.5)
        c: эффективность охоты хищника (0.01-0.06)
        beta: скорость гибели хищников от голода (0.4-1.5)
        d: вклад съеденной жертвы в размножение хищников (0.01-0.06)
        T: длительность моделирования (5-50 лет)
        N: количество шагов интегрирования (200-10000)
        seed: зерно для воспроизводимости
    
    Возвращает:
        SimulationResult с историей популяций и аналитическими данными
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Вычисляем шаг по времени
    dt = T / N
    
    # Создаем массивы для результатов
    time = np.zeros(N + 1)
    prey = np.zeros(N + 1)
    predators = np.zeros(N + 1)
    
    # Начальные условия
    time[0] = 0
    prey[0] = x0
    predators[0] = y0
    
    # Численное интегрирование методом Эйлера
    for i in range(N):
        # Вычисляем приращения
        dx_dt = alpha * prey[i] - c * prey[i] * predators[i]
        dy_dt = d * prey[i] * predators[i] - beta * predators[i]
        
        # Шаг метода Эйлера
        prey_next = prey[i] + dx_dt * dt
        predators_next = predators[i] + dy_dt * dt
        
        # Обработка отрицательных значений (биологическая корректность)
        prey[i + 1] = max(prey_next, 0)
        predators[i + 1] = max(predators_next, 0)
        time[i + 1] = time[i] + dt
    
    # Аналитический расчет равновесия
    equilibrium_prey = beta / d if d > 0 else 0
    equilibrium_predator = alpha / c if c > 0 else 0
    
    # Расчет периода малых колебаний
    period = 2 * np.pi / np.sqrt(alpha * beta) if alpha * beta > 0 else 0
    
    # Определение типа устойчивости
    # Для классической модели Лотки-Вольтерры - центр
    stability_type = "Центр (консервативные колебания)"
    
    # Средние значения
    avg_prey = np.mean(prey)
    avg_predator = np.mean(predators)
    
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


def plot_dynamics(
    result: SimulationResult,
    save_path: Optional[str] = None
) -> str:
    """
    Построение графиков динамики популяций и фазового портрета.
    
    Параметры:
        result: результат симуляции
        save_path: путь для сохранения графика (опционально)
    
    Возвращает:
        base64-строку с изображением для вставки в HTML
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # График 1: Динамика численности во времени
    ax1 = axes[0]
    ax1.plot(result.time, result.prey, 'g-', label='Жертвы (кролики)', linewidth=2)
    ax1.plot(result.time, result.predators, 'r-', label='Хищники (лисы)', linewidth=2)
    ax1.axhline(y=result.equilibrium_prey, color='g', linestyle='--', alpha=0.5, 
                label=f'Равновесие жертв: {result.equilibrium_prey:.1f}')
    ax1.axhline(y=result.equilibrium_predator, color='r', linestyle='--', alpha=0.5,
                label=f'Равновесие хищников: {result.equilibrium_predator:.1f}')
    ax1.set_xlabel('Время (годы)')
    ax1.set_ylabel('Численность')
    ax1.set_title('Динамика популяций во времени')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График 2: Фазовый портрет
    ax2 = axes[1]
    ax2.plot(result.prey, result.predators, 'b-', linewidth=1.5, alpha=0.7)
    ax2.plot(result.prey[0], result.predators[0], 'go', markersize=10, label='Старт')
    ax2.plot(result.prey[-1], result.predators[-1], 'ro', markersize=10, label='Финиш')
    ax2.plot(result.equilibrium_prey, result.equilibrium_predator, 'bo', markersize=8, 
             label='Равновесие')
    ax2.set_xlabel('Численность жертв')
    ax2.set_ylabel('Численность хищников')
    ax2.set_title('Фазовый портрет системы')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=result.equilibrium_predator, color='r', linestyle='--', alpha=0.3)
    ax2.axvline(x=result.equilibrium_prey, color='g', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    # Конвертация в base64 для веб-страницы
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_base64


def analyze_scenario(
    x0: float = 50.0,
    y0: float = 10.0,
    alpha: float = 0.8,
    c: float = 0.03,
    beta: float = 0.6,
    d: float = 0.02,
    T: float = 50.0,
    N: int = 1000
) -> dict:
    """
    Анализ сценария модели с выводом характеристик.
    
    Возвращает:
        Словарь с параметрами и результатами анализа
    """
    result = simulate_lotka_volterra(
        x0=x0, y0=y0, alpha=alpha, c=c, beta=beta, d=d, T=T, N=N
    )
    
    # Проверка на реалистичность результата
    is_realistic = (
        max(result.prey) < 500 and 
        max(result.predators) < 200 and
        min(result.prey) >= 0 and
        min(result.predators) >= 0
    )
    
    return {
        'parameters': {
            'x0 (жертвы нач.)': x0,
            'y0 (хищники нач.)': y0,
            'α (рождаемость жертв)': alpha,
            'c (эффективность охоты)': c,
            'β (смертность хищников)': beta,
            'd (рождаемость хищников)': d,
            'T (время симуляции)': T,
            'N (шагов)': N
        },
        'equilibrium': {
            'x* (равновесные жертвы)': result.equilibrium_prey,
            'y* (равновесные хищники)': result.equilibrium_predator
        },
        'dynamics': {
            'Период колебаний': result.period,
            'Тип устойчивости': result.stability_type,
            'Ср. численность жертв': result.avg_prey,
            'Ср. численность хищников': result.avg_predator
        },
        'bio_check': {
            'Реалистичность': 'Да' if is_realistic else 'Нет',
            'Мин. жертвы': min(result.prey),
            'Макс. жертвы': max(result.prey),
            'Мин. хищники': min(result.predators),
            'Макс. хищники': max(result.predators)
        },
        'result': result
    }


def compare_parameters(
    base_params: dict,
    param_to_vary: str,
    values: List[float],
    T: float = 50.0,
    N: int = 1000
) -> dict:
    """
    Сравнение поведения модели при изменении параметра.
    
    Параметры:
        base_params: базовые параметры (x0, y0, alpha, c, beta, d)
        param_to_vary: имя изменяемого параметра ('alpha', 'c', 'beta', 'd')
        values: список значений для перебора
        T, N: параметры симуляции
    
    Возвращает:
        Результаты сравнения
    """
    results = []
    
    for val in values:
        params = base_params.copy()
        params[param_to_vary] = val
        
        result = simulate_lotka_volterra(
            x0=params.get('x0', 50),
            y0=params.get('y0', 10),
            alpha=params.get('alpha', 0.8),
            c=params.get('c', 0.03),
            beta=params.get('beta', 0.6),
            d=params.get('d', 0.02),
            T=T, N=N
        )
        
        results.append({
            'param_value': val,
            'equilibrium_prey': result.equilibrium_prey,
            'equilibrium_predator': result.equilibrium_predator,
            'period': result.period,
            'avg_prey': result.avg_prey,
            'avg_predator': result.avg_predator
        })
    
    return {
        'param_name': param_to_vary,
        'values': values,
        'results': results
    }


# ---------- Демо-запуск ----------
if __name__ == '__main__':
    print("=" * 60)
    print("Модель «Хищник-жертва» (Лотки-Вольтерры)")
    print("=" * 60)
    
    # Базовый сценарий
    print("\n>>> Базовый сценарий:")
    scenario = analyze_scenario(
        x0=50, y0=10, alpha=0.8, c=0.03, beta=0.6, d=0.02, T=50, N=1000
    )
    
    print(f"\n--- ПАРАМЕТРЫ ---")
    for key, val in scenario['parameters'].items():
        print(f"{key}: {val}")
    
    print(f"\n--- РАВНОВЕСИЕ ---")
    for key, val in scenario['equilibrium'].items():
        print(f"{key}: {val:.2f}")
    
    print(f"\n--- ДИНАМИКА ---")
    for key, val in scenario['dynamics'].items():
        print(f"{key}: {val}")
    
    print(f"\n--- БИОЛОГИЧЕСКАЯ КОРРЕКТНОСТЬ ---")
    for key, val in scenario['bio_check'].items():
        print(f"{key}: {val}")
    
    # Сравнение при изменении параметров
    print("\n>>> Сравнение при изменении α (рождаемости жертв):")
    base = {'x0': 50, 'y0': 10, 'alpha': 0.8, 'c': 0.03, 'beta': 0.6, 'd': 0.02}
    comparison = compare_parameters(base, 'alpha', [0.5, 0.8, 1.2], T=50, N=1000)
    
    for res in comparison['results']:
        print(f"α = {res['param_value']:.1f}: "
              f"жертвы = {res['equilibrium_prey']:.1f}, "
              f"хищники = {res['equilibrium_predator']:.1f}, "
              f"период = {res['period']:.1f}")