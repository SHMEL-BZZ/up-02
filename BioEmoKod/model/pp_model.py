import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Optional
import io
import base64

# Импорт расчетной логики из отдельного модуля
from controller.pp_controller import simulate_lotka_volterra, SimulationResult


def plot_dynamics(
    result: SimulationResult,
    save_path: Optional[str] = None
) -> str:
    """
    Функция визуализации результатов моделирования
    """
    # Создаем фигуру с двумя подграфиками (1 строка, 2 колонки, размер 14x5 дюймов)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # ========== ГРАФИК 1: Динамика численности во времени ==========
    ax1 = axes[0]
    
    # Отображаем динамику популяций
    ax1.plot(result.time, result.prey, 'g-', label='Жертвы (кролики)', linewidth=2)
    ax1.plot(result.time, result.predators, 'r-', label='Хищники (лисы)', linewidth=2)
    
    # Пунктирными линиями показываем равновесные значения
    ax1.axhline(y=result.equilibrium_prey, color='g', linestyle='--', alpha=0.5, 
                label=f'Равновесие жертв: {result.equilibrium_prey:.1f}')
    ax1.axhline(y=result.equilibrium_predator, color='r', linestyle='--', alpha=0.5,
                label=f'Равновесие хищников: {result.equilibrium_predator:.1f}')
    
    # Настройка подписей и внешнего вида
    ax1.set_xlabel('Время (годы)')
    ax1.set_ylabel('Численность')
    ax1.set_title('Динамика популяций во времени')
    ax1.legend()
    ax1.grid(True, alpha=0.3)  # Сетка с прозрачностью 30%
    
    # ========== ГРАФИК 2: Фазовый портрет ==========
    ax2 = axes[1]
    
    # Фазовая траектория - показывает взаимосвязь популяций
    ax2.plot(result.prey, result.predators, 'b-', linewidth=1.5, alpha=0.7)
    
    # Отмечаем начальную и конечную точки
    ax2.plot(result.prey[0], result.predators[0], 'go', markersize=10, label='Старт')
    ax2.plot(result.prey[-1], result.predators[-1], 'ro', markersize=10, label='Финиш')
    
    # Точка равновесия (особая точка системы)
    ax2.plot(result.equilibrium_prey, result.equilibrium_predator, 'bo', markersize=8, 
             label='Равновесие')
    
    # Настройка фазового портрета
    ax2.set_xlabel('Численность жертв')
    ax2.set_ylabel('Численность хищников')
    ax2.set_title('Фазовый портрет системы')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Вспомогательные линии, показывающие равновесные значения на осях
    ax2.axhline(y=result.equilibrium_predator, color='r', linestyle='--', alpha=0.3)
    ax2.axvline(x=result.equilibrium_prey, color='g', linestyle='--', alpha=0.3)
    
    # Автоматическая подгонка расположения элементов
    plt.tight_layout()
    
    # Сохраняем в файл, если указан путь
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    # Конвертация в base64 для вставки в HTML/веб-страницы
    # Это полезно для Jupyter Notebook, веб-приложений (Streamlit, Django, Flask)
    buf = io.BytesIO()  # Создаем буфер в памяти
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')  # Рисуем в буфер
    buf.seek(0)  # Перемещаем указатель в начало буфера
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')  # Кодируем в base64
    plt.close()  # Закрываем фигуру для освобождения памяти
    
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
    📈 Комплексный анализ одного сценария модели
    
    Что делает:
    1. Запускает симуляцию с заданными параметрами
    2. Проверяет биологическую реалистичность результата
    3. Формирует структурированный отчет со всеми характеристиками
    
    Возвращаемый словарь содержит 5 разделов:
    - 'parameters': входные параметры модели
    - 'equilibrium': теоретические равновесные значения
    - 'dynamics': характеристики колебательного процесса
    - 'bio_check': проверка на биологическую корректность
    - 'result': полный объект SimulationResult
    
    Пример использования:
    >>> analysis = analyze_scenario(x0=30, alpha=1.2, T=100)
    >>> print(analysis['equilibrium']['x* (равновесные жертвы)'])
    """
    # Запуск симуляции (расчетная логика в pp_controller.py)
    result = simulate_lotka_volterra(
        x0=x0, y0=y0, alpha=alpha, c=c, beta=beta, d=d, T=T, N=N
    )
    
    # ✅ Проверка на реалистичность
    # Критерии: популяции не выходят за разумные пределы и не становятся отрицательными
    is_realistic = (
        max(result.prey) < 500 and      # Жертв не слишком много
        max(result.predators) < 200 and  # Хищников не слишком много
        min(result.prey) >= 0 and        # Нет отрицательных значений
        min(result.predators) >= 0
    )
    
    # Структурированный возврат данных
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
        'result': result  # Сохраняем полный результат для дальнейшей визуализации
    }


def compare_parameters(
    base_params: dict,
    param_to_vary: str,
    values: List[float],
    T: float = 50.0,
    N: int = 1000
) -> dict:
    """
    🔬 Анализ чувствительности модели к изменению параметров
    
    Что делает:
    - Проводит серию симуляций, меняя один параметр
    - Позволяет увидеть, как параметр влияет на поведение системы
    
    Параметры:
        base_params: базовый набор параметров {'x0':50, 'y0':10, 'alpha':0.8, ...}
        param_to_vary: имя параметра для изменения ('alpha', 'c', 'beta', 'd')
        values: список значений параметра для тестирования
        T, N: параметры симуляции
    
    Возвращает:
        Словарь с результатами сравнения для анализа чувствительности
    
    Пример:
    >>> base = {'x0': 50, 'y0': 10, 'alpha': 0.8, 'c': 0.03, 'beta': 0.6, 'd': 0.02}
    >>> сравнение = compare_parameters(base, 'alpha', [0.5, 0.8, 1.2])
    >>> for res in сравнение['results']:
    >>>     print(f"α={res['param_value']}: равновесие={res['equilibrium_prey']:.1f}")
    """
    results = []
    
    # Перебираем все значения параметра
    for val in values:
        # Создаем копию базовых параметров и изменяем нужный
        params = base_params.copy()
        params[param_to_vary] = val
        
        # Запускаем симуляцию с новыми параметрами
        result = simulate_lotka_volterra(
            x0=params.get('x0', 50),
            y0=params.get('y0', 10),
            alpha=params.get('alpha', 0.8),
            c=params.get('c', 0.03),
            beta=params.get('beta', 0.6),
            d=params.get('d', 0.02),
            T=T, N=N
        )
        
        # Сохраняем ключевые характеристики для этого значения параметра
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


