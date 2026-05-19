"""
Модуль с расчетной логикой модели "Распространение эпидемии"
Для независимого тестирования и использования в других файлах
"""

import random
import numpy as np # для математических операций
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional 


@dataclass
class SimulationResult:
    """Результат симуляции эпидемии."""
    history_s: List[int]          # История здоровых крыс
    history_i: List[int]          # История зараженных крыс
    history_r: List[int]          # История иммунных крыс
    weekly_infections: List[int]  # Еженедельные заражения
    threshold: float              # Эпидемический порог
    efficacy: float               # Эффективность вакцинации (%)
    peak_without: int             # Пик заражения без вакцинации
    peak_with: int                # Пик заражения с вакцинацией
    week_without: int             # Неделя пика без вакцинации
    week_with: int                # Неделя пика с вакцинацией
    matrix_display: List[List[List[str]]]  # Состояние сетки для отображения
    n: int                        # Размер сетки
    epidemic_weeks_without: int   # Количество эпидемических недель без вакцинации
    epidemic_weeks_with: int      # Количество эпидемических недель с вакцинацией


def calculate_epidemic_threshold(weekly_infections: List[int]) -> float:
    """
    Расчет эпидемического порога по первым 8 неделям.
    
    Параметры:
        weekly_infections: список еженедельных заражений
    
    Возвращает:
        эпидемический порог (mean + 2.507 * std)
    """
    if len(weekly_infections) >= 8:
        first_8 = weekly_infections[:8]
        mean = np.mean(first_8)
        std = np.std(first_8, ddof=1) if len(first_8) > 1 else 0
        threshold = mean + 2.507 * std
        return round(threshold, 1)
    return 0


def count_epidemic_weeks(infected_history: List[int], threshold: float) -> int:
    """
    Подсчёт количества эпидемических недель.
    
    Эпидемическая неделя - неделя, когда количество заражённых > порога.
    
    Параметры:
        infected_history: история количества заражённых по неделям
        threshold: эпидемический порог
    
    Возвращает:
        количество эпидемических недель
    """
    return sum(1 for infected in infected_history if infected > threshold)


def calculate_efficacy(epidemic_weeks_without: int, epidemic_weeks_with: int) -> float:
    """
    Расчет эффективности вакцинации на основе эпидемических недель.
    
    Параметры:
        epidemic_weeks_without: количество эпидемических недель без вакцинации
        epidemic_weeks_with: количество эпидемических недель с вакцинацией
    
    Возвращает:
        эффективность в процентах
    """
    if epidemic_weeks_without == 0:
        return 0.0
    
    efficacy = (epidemic_weeks_without - epidemic_weeks_with) / epidemic_weeks_without * 100
    
    # Эффективность не может быть ниже 0%
    return round(max(0, efficacy), 1)


def create_empty_grid(n: int) -> List[List[List[int]]]:
    """
    Создание пустой сетки.
    
    Параметры:
        n: размер сетки
    
    Возвращает:
        пустая сетка (список списков списков)
    """
    return [[[] for _ in range(n)] for _ in range(n)]


def initialize_rats(
    n: int, 
    total_rats: int, 
    max_per_cell: int = 4
) -> Tuple[List[List[List[int]]], Dict[int, Dict]]:
    """
    Инициализация сетки и размещение крыс.
    
    Параметры:
        n: размер сетки
        total_rats: общее количество крыс
        max_per_cell: максимальное количество крыс в одной клетке
    
    Возвращает:
        (grid, rats_data) - сетка и данные о крысах
    """
    grid = create_empty_grid(n)
    rats_data = {}
    
    rats_placed = 0
    while rats_placed < total_rats:
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        if len(grid[x][y]) < max_per_cell:
            rat_id = rats_placed
            rats_data[rat_id] = {
                'status': 'S',
                'counter': 0,
                'pos': (x, y)
            }
            grid[x][y].append(rat_id)
            rats_placed += 1
    
    # Заражаем одну случайную крысу
    rat_ids = list(rats_data.keys())
    if rat_ids:
        infected_id = random.choice(rat_ids)
        rats_data[infected_id]['status'] = 'I'
        rats_data[infected_id]['counter'] = 1
    
    return grid, rats_data


def move_rats(
    grid: List[List[List[int]]], 
    rats_data: Dict[int, Dict], 
    p_move: float,
    n: int,
    max_per_cell: int = 4
) -> Tuple[List[List[List[int]]], Dict[int, Dict]]:
    """
    Перемещение крыс.
    
    Параметры:
        grid: текущая сетка
        rats_data: данные о крысах
        p_move: вероятность перемещения
        n: размер сетки
        max_per_cell: максимальное количество крыс в клетке
    
    Возвращает:
        (new_grid, rats_data) - обновленная сетка и данные
    """
    new_grid = [[[] for _ in range(n)] for _ in range(n)]
    
    # Копируем текущие позиции
    for x in range(n):
        for y in range(n):
            for rat_id in grid[x][y]:
                new_grid[x][y].append(rat_id)
    
    # Перемещаем крыс
    for x in range(n):
        for y in range(n):
            for rat_id in grid[x][y]:
                if random.random() < p_move:
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and len(new_grid[nx][ny]) < max_per_cell:
                        new_grid[x][y].remove(rat_id)
                        new_grid[nx][ny].append(rat_id)
                        rats_data[rat_id]['pos'] = (nx, ny)
    
    return new_grid, rats_data


def infect_rats(
    grid: List[List[List[int]]], 
    rats_data: Dict[int, Dict], 
    p_infect: float
) -> Dict[int, Dict]:
    """
    Процесс заражения.
    
    Параметры:
        grid: текущая сетка
        rats_data: данные о крысах
        p_infect: вероятность заражения
    
    Возвращает:
        обновленные данные о крысах
    """
    infected_cells = set()
    
    # Находим клетки с зараженными крысами
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for rat_id in grid[x][y]:
                if rats_data[rat_id]['status'] == 'I':
                    infected_cells.add((x, y))
    
    # Заражение здоровых крыс в зараженных клетках
    for x, y in infected_cells:
        for rat_id in grid[x][y]:
            if rats_data[rat_id]['status'] == 'S' and random.random() < p_infect:
                rats_data[rat_id]['status'] = 'I'
                rats_data[rat_id]['counter'] = 1
    
    return rats_data


def update_statuses(
    rats_data: Dict[int, Dict], 
    ill_days: int = 6, 
    immun_days: int = 4
) -> Dict[int, Dict]:
    """
    Обновление статусов (болезнь, иммунитет).
    
    Параметры:
        rats_data: данные о крысах
        ill_days: длительность болезни в днях
        immun_days: длительность иммунитета в днях
    
    Возвращает:
        обновленные данные о крысах
    """
    for rat_id in rats_data:
        status = rats_data[rat_id]['status']
        counter = rats_data[rat_id]['counter']
        
        if status == 'I':
            if counter >= ill_days:
                rats_data[rat_id]['status'] = 'R'
                rats_data[rat_id]['counter'] = 1
            else:
                rats_data[rat_id]['counter'] += 1
        elif status == 'R':
            if counter >= immun_days:
                rats_data[rat_id]['status'] = 'S'
                rats_data[rat_id]['counter'] = 0
            else:
                rats_data[rat_id]['counter'] += 1
    
    return rats_data


def vaccinate(
    rats_data: Dict[int, Dict], 
    day: int, 
    vacc_day: int, 
    vacc_percent: int
) -> Dict[int, Dict]:
    """
    Вакцинация в заданный день.
    
    Параметры:
        rats_data: данные о крысах
        day: текущий день
        vacc_day: день вакцинации
        vacc_percent: процент вакцинируемых крыс
    
    Возвращает:
        обновленные данные о крысах
    """
    if day == vacc_day:
        healthy_ids = [rid for rid, d in rats_data.items() if d['status'] == 'S']
        target = int(len(healthy_ids) * vacc_percent / 100)
        if target > 0 and healthy_ids:
            to_vacc = random.sample(healthy_ids, min(target, len(healthy_ids)))
            for rid in to_vacc:
                rats_data[rid]['status'] = 'R'
                rats_data[rid]['counter'] = 1
    
    return rats_data


def record_stats(
    rats_data: Dict[int, Dict], 
    history: Dict[str, List[int]], 
    weekly_infections: List[int], 
    week: int
) -> Tuple[Dict[str, List[int]], List[int]]:
    """
    Запись статистики по неделям.
    
    Параметры:
        rats_data: данные о крысах
        history: история статусов
        weekly_infections: список еженедельных заражений
        week: номер недели
    
    Возвращает:
        (history, weekly_infections) - обновленные данные
    """
    s = sum(1 for d in rats_data.values() if d['status'] == 'S')
    i = sum(1 for d in rats_data.values() if d['status'] == 'I')
    r = sum(1 for d in rats_data.values() if d['status'] == 'R')
    
    history['S'].append(s)
    history['I'].append(i)
    history['R'].append(r)
    
    # Расчет новых заражений за неделю
    if week > 0 and len(history['I']) > 1:
        infections_this_week = max(0, i - history['I'][week-1] + r - (history['R'][week-1] if len(history['R']) > 1 else 0))
        weekly_infections.append(infections_this_week)
    else:
        weekly_infections.append(i)
    
    return history, weekly_infections


def get_matrix_state(
    grid: List[List[List[int]]], 
    rats_data: Dict[int, Dict], 
    n: int
) -> List[List[Dict[str, int]]]:
    """
    Получение текущего состояния матрицы для визуализации.
    
    Параметры:
        grid: текущая сетка
        rats_data: данные о крысах
        n: размер сетки
    
    Возвращает:
        матрица состояния (счетчики S/I/R в каждой клетке)
    """
    matrix = [[{'S': 0, 'I': 0, 'R': 0} for _ in range(n)] for _ in range(n)]
    for rat_id, data in rats_data.items():
        x, y = data['pos']
        status = data['status']
        matrix[x][y][status] += 1
    return matrix


def matrix_to_display(matrix_state: List[List[Dict[str, int]]]) -> List[List[List[str]]]:
    """
    Преобразует matrix_state в список статусов для отображения точек.
    
    Параметры:
        matrix_state: матрица состояния
    
    Возвращает:
        матрица для отображения (списки статусов в каждой клетке)
    """
    n = len(matrix_state)
    matrix_display = []
    for i in range(n):
        row = []
        for j in range(n):
            cell = matrix_state[i][j]
            statuses = []
            for _ in range(cell['S']):
                statuses.append('S')
            for _ in range(cell['I']):
                statuses.append('I')
            for _ in range(cell['R']):
                statuses.append('R')
            row.append(statuses)
        matrix_display.append(row)
    return matrix_display


def run_single_simulation(
    n: int,
    total_rats: int,
    weeks: int,
    p_infect: float,
    p_move: float,
    vacc_day: Optional[int],
    vacc_percent: Optional[int],
    max_per_cell: int,
    ill_days: int,
    immun_days: int,
    return_matrix: bool = False
) -> tuple:
    """
    Запуск одной симуляции с возможностью сохранения финальной матрицы.
    
    Возвращает:
        (history_s, history_i, history_r, weekly_infections, threshold, matrix_display)
    """
    # Инициализация
    grid, rats_data = initialize_rats(n, total_rats, max_per_cell)
    history = {'S': [], 'I': [], 'R': []}
    weekly_infections = []
    
    total_days = weeks * 7
    current_week = 0
    
    # Основной цикл симуляции
    for day in range(total_days):
        # Вакцинация (если включена)
        if vacc_day is not None and vacc_percent is not None:
            rats_data = vaccinate(rats_data, day, vacc_day, vacc_percent)
        
        # Шаги симуляции
        grid, rats_data = move_rats(grid, rats_data, p_move, n, max_per_cell)
        rats_data = infect_rats(grid, rats_data, p_infect)
        rats_data = update_statuses(rats_data, ill_days, immun_days)
        
        # Запись статистики по неделям
        if day % 7 == 0:
            history, weekly_infections = record_stats(
                rats_data, history, weekly_infections, current_week
            )
            current_week += 1
    
    # Расчет порога
    threshold = calculate_epidemic_threshold(weekly_infections)
    
    # Получаем матрицу для отображения (если нужно)
    matrix_display = None
    if return_matrix:
        matrix_state = get_matrix_state(grid, rats_data, n)
        matrix_display = matrix_to_display(matrix_state)
    
    return (
        history['S'], history['I'], history['R'],
        weekly_infections, threshold, matrix_display
    )


def simulate_epidemic(
    n: int,
    total_rats: int,
    weeks: int,
    p_infect: float,
    p_move: float,
    vacc_day: int,
    vacc_percent: int,
    max_per_cell: int = 4,
    ill_days: int = 6,
    immun_days: int = 4,
) -> SimulationResult:
    """
    Основная функция симуляции эпидемии.
    
    Параметры:
        n: размер сетки
        total_rats: общее количество крыс
        weeks: количество недель
        p_infect: вероятность заражения
        p_move: вероятность перемещения
        vacc_day: день вакцинации
        vacc_percent: процент вакцинации
        max_per_cell: максимальное количество крыс в клетке
        ill_days: длительность болезни
        immun_days: длительность иммунитета
    
    Возвращает:
        SimulationResult с результатами симуляции
    """

    # Сохраняем начальное состояние для идентичных условий
    saved_random_state = random.getstate()
    saved_np_state = np.random.get_state()
    
    # ===== СИМУЛЯЦИЯ БЕЗ вакцинации =====
    s_without, i_without, r_without, weekly_without, threshold_without, _ = run_single_simulation(
    n, total_rats, weeks, p_infect, p_move,
    None, None,
    max_per_cell, ill_days, immun_days,
    False
    )
    
    # Подсчёт эпидемических недель без вакцинации
    epidemic_weeks_without = count_epidemic_weeks(i_without, threshold_without)
    
    # Восстанавливаем состояние для идентичных начальных условий
    random.setstate(saved_random_state)
    np.random.set_state(saved_np_state)
    
    # ===== СИМУЛЯЦИЯ С вакцинацией =====
    s_with, i_with, r_with, weekly_with, threshold_with, matrix_display = run_single_simulation(
    n, total_rats, weeks, p_infect, p_move,
    vacc_day, vacc_percent,
    max_per_cell, ill_days, immun_days,
    True
    )
    
    # Подсчёт эпидемических недель с вакцинацией
    epidemic_weeks_with = count_epidemic_weeks(i_with, threshold_with)
    
    # Находим пики
    peak_without = max(i_without) if i_without else 0
    peak_with = max(i_with) if i_with else 0
    week_without = i_without.index(peak_without) if peak_without in i_without else 0
    week_with = i_with.index(peak_with) if peak_with in i_with else 0
    
    # Расчет эффективности ПО ЭПИДЕМИЧЕСКИМ НЕДЕЛЯМ
    efficacy = calculate_efficacy(epidemic_weeks_without, epidemic_weeks_with)
    
    return SimulationResult(
        history_s=s_with,
        history_i=i_with,
        history_r=r_with,
        weekly_infections=weekly_with,
        threshold=threshold_with,
        efficacy=efficacy,
        peak_without=peak_without,
        peak_with=peak_with,
        week_without=week_without,
        week_with=week_with,
        matrix_display=matrix_display,
        n=n,
        epidemic_weeks_without=epidemic_weeks_without,
        epidemic_weeks_with=epidemic_weeks_with
    )