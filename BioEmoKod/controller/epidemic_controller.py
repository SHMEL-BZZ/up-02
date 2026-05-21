import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Optional, List, Dict
import numpy as np

# Импорт расчетной логики из отдельного модуля
from model.epidemic import simulate_epidemic, SimulationResult


def plot_epidemic_dynamics(
    result: SimulationResult,
    vacc_day: int,
    weeks: int,
    save_path: Optional[str] = None
) -> str:
    """
    Функция визуализации результатов моделирования эпидемии.
    
    Параметры:
        result: результат симуляции (SimulationResult)
        vacc_day: день вакцинации
        weeks: количество недель
        save_path: путь для сохранения (опционально)
    
    Возвращает:
        base64 строку с изображением графика
    """
    # Создаем фигуру
    plt.figure(figsize=(12, 6))
    
    # Недели для оси X
    weeks_range = list(range(len(result.history_s)))
    
    # Графики S, I, R
    plt.plot(weeks_range, result.history_s, 'g-', label='S (здоровые)', linewidth=2)
    plt.plot(weeks_range, result.history_i, 'r-', label='I (заражённые)', linewidth=2)
    plt.plot(weeks_range, result.history_r, 'y-', label='R (иммунные)', linewidth=2)
    
    # Линия вакцинации
    vacc_week = vacc_day / 7
    if 0 <= vacc_week <= weeks:
        plt.axvline(x=vacc_week, color='purple', linestyle='--', linewidth=2, label='Вакцинация')
    
    # Отметка пика заражения
    peak_week = result.week_with
    peak_value = result.peak_with
    plt.plot(peak_week, peak_value, 'ro', markersize=10, label=f'Пик заражения: нед. {peak_week}, {peak_value} крыс')
    
    # Настройка подписей и внешнего вида
    plt.xlabel('Недели', fontsize=12)
    plt.ylabel('Количество крыс', fontsize=12)
    plt.title('Динамика распространения эпидемии (модель SIR)', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Сохраняем в файл, если указан путь
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    # Конвертация в base64 для вставки в HTML
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_base64}"


def plot_comparison_chart(
    result_with: SimulationResult,
    result_without: SimulationResult,
    vacc_day: int,
    weeks: int,
    save_path: Optional[str] = None
) -> str:
    """
    Сравнительный график с вакцинацией и без.
    
    Параметры:
        result_with: результат с вакцинацией
        result_without: результат без вакцинации
        vacc_day: день вакцинации
        weeks: количество недель
        save_path: путь для сохранения
    
    Возвращает:
        base64 строку с изображением графика
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    weeks_range = list(range(len(result_without.history_i)))
    vacc_week = vacc_day / 7
    
    # График без вакцинации
    ax1.plot(weeks_range, result_without.history_i, 'r-', linewidth=2, label='Заражённые')
    ax1.plot(weeks_range, result_without.history_s, 'g-', linewidth=1.5, alpha=0.7, label='Здоровые')
    ax1.plot(weeks_range, result_without.history_r, 'y-', linewidth=1.5, alpha=0.7, label='Иммунные')
    ax1.set_xlabel('Недели')
    ax1.set_ylabel('Количество крыс')
    ax1.set_title('Без вакцинации')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График с вакцинацией
    ax2.plot(weeks_range, result_with.history_i, 'r-', linewidth=2, label='Заражённые')
    ax2.plot(weeks_range, result_with.history_s, 'g-', linewidth=1.5, alpha=0.7, label='Здоровые')
    ax2.plot(weeks_range, result_with.history_r, 'y-', linewidth=1.5, alpha=0.7, label='Иммунные')
    if 0 <= vacc_week <= weeks:
        ax2.axvline(x=vacc_week, color='purple', linestyle='--', linewidth=2, label='Вакцинация')
    ax2.set_xlabel('Недели')
    ax2.set_ylabel('Количество крыс')
    ax2.set_title(f'С вакцинацией (эффективность: {result_with.efficacy}%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Сравнение динамики эпидемии', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Сохраняем и конвертируем
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_base64}"


def analyze_epidemic_scenario(
    n: int,
    total_rats: int,
    weeks: int,
    p_infect: float,
    p_move: float,
    vacc_day: int,
    vacc_percent: int,
    record_history: bool = True
) -> dict:
    """
    Комплексный анализ одного сценария эпидемии.
    
    Что делает:
    1. Запускает симуляцию с заданными параметрами
    2. Рассчитывает ключевые показатели
    3. Формирует структурированный отчет
    
    Возвращаемый словарь содержит:
    - 'parameters': входные параметры модели
    - 'results': основные результаты симуляции
    - 'evaluation': оценка эффективности вакцинации
    - 'simulation_result': полный объект SimulationResult
    - 'graph': base64 график для отображения
    
    Пример использования:
    >>> analysis = analyze_epidemic_scenario(n=8, total_rats=64, weeks=52, ...)
    >>> print(analysis['evaluation']['Эффективность вакцинации'])
    """
    # Запуск симуляции (расчетная логика в epidemic_controller.py)
    result = simulate_epidemic(
        n=n,
        total_rats=total_rats,
        weeks=weeks,
        p_infect=p_infect,
        p_move=p_move,
        vacc_day=vacc_day,
        vacc_percent=vacc_percent,
        record_history=record_history
    )
    
    # Запуск симуляции без вакцинации для сравнения
    result_without = simulate_epidemic(
        n=n,
        total_rats=total_rats,
        weeks=weeks,
        p_infect=p_infect,
        p_move=p_move,
        vacc_day=weeks * 7 + 1,  # Вакцинация после окончания (фактически без вакцинации)
        vacc_percent=vacc_percent,
    )
    
    # Проверка на реалистичность
    is_realistic = (
        max(result.history_i) < total_rats * 0.9 and  # Пик не превышает 90% популяции
        min(result.history_s) >= 0 and
        min(result.history_i) >= 0
    )
    
    # Генерация графика
    graph_base64 = plot_epidemic_dynamics(result, vacc_day, weeks)
    
    return {
        'parameters': {
            'Размер сетки (n)': n,
            'Общее число крыс': total_rats,
            'Длительность (недели)': weeks,
            'Вероятность заражения': round(p_infect, 1),
            'Вероятность перемещения': round(p_move, 1),
            'День вакцинации': vacc_day,
            'Процент вакцинации': f"{vacc_percent}%"
        },
        'results': {
            'Эпидемический порог': result.threshold,
            'Пик заражения (с вакцинацией)': result.peak_with,
            'Неделя пика (с вакцинацией)': result.week_with,
            'Пик заражения (без вакцинации)': result.peak_without,
            'Неделя пика (без вакцинации)': result.week_without,
            'Эпидемические недели (без вакцинации)': result.epidemic_weeks_without,
            'Эпидемические недели (с вакцинацией)': result.epidemic_weeks_with,
            'Всего заражений за период': sum(result.weekly_infections)
        },
        'evaluation': {
            'Эффективность вакцинации': f"{result.efficacy}%",
            'Реалистичность сценария': 'Да' if is_realistic else 'Нет'
        },
        'simulation_result': result,
        'graph': graph_base64,
        'comparison_graph': plot_comparison_chart(result, result_without, vacc_day, weeks)
    }