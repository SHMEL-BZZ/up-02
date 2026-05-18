import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from datetime import datetime

class EpidemicSimulation:
    def __init__(self, params):
        """
        Инициализация симуляции.
        params: словарь с параметрами из формы
        """
        self.n = int(params['grid_size'])
        self.total_rats = int(params['total_rats'])
        self.weeks = int(params['weeks'])
        self.p_infect = float(params['p_infect'])
        self.p_move = float(params['p_move'])
        self.vacc_day = int(params['vacc_day'])
        self.vacc_percent = int(params['vacc_percent'])
        
        # Фиксированные параметры
        self.ILL_DAYS = 6
        self.IMMUN_DAYS = 4
        self.MAX_PER_CELL = 4
        
        # Сетка и состояние крыс
        self.grid = None
        self.rats_data = {}
        
        # Результаты симуляции
        self.history = {'S': [], 'I': [], 'R': []}
        self.weekly_infections = []
        
        # Для сравнения вакцинации
        self.efficacy = 0
        self.peaks = {'without': 0, 'with': 0, 'week_without': 0, 'week_with': 0}
        
        # Запускаем основную симуляцию
        self.run()
    
    def _init_grid(self):
        """Инициализация пустой сетки и размещение крыс"""
        self.grid = [[[] for _ in range(self.n)] for _ in range(self.n)]
        self.rats_data = {}
        
        # Размещаем крыс случайно
        rats_placed = 0
        while rats_placed < self.total_rats:
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            if len(self.grid[x][y]) < self.MAX_PER_CELL:
                rat_id = rats_placed
                self.rats_data[rat_id] = {
                    'status': 'S',
                    'counter': 0,
                    'pos': (x, y)
                }
                self.grid[x][y].append(rat_id)
                rats_placed += 1
        
        # Заражаем одну случайную крысу
        rat_ids = list(self.rats_data.keys())
        if rat_ids:
            infected_id = random.choice(rat_ids)
            self.rats_data[infected_id]['status'] = 'I'
            self.rats_data[infected_id]['counter'] = 1
    
    def _move_rats(self):
        """Перемещение крыс"""
        new_grid = [[[] for _ in range(self.n)] for _ in range(self.n)]
        for x in range(self.n):
            for y in range(self.n):
                for rat_id in self.grid[x][y]:
                    new_grid[x][y].append(rat_id)
        
        for x in range(self.n):
            for y in range(self.n):
                for rat_id in self.grid[x][y]:
                    if random.random() < self.p_move:
                        dx = random.randint(-1, 1)
                        dy = random.randint(-1, 1)
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.n and 0 <= ny < self.n and len(new_grid[nx][ny]) < self.MAX_PER_CELL:
                            new_grid[x][y].remove(rat_id)
                            new_grid[nx][ny].append(rat_id)
                            self.rats_data[rat_id]['pos'] = (nx, ny)
        self.grid = new_grid
    
    def _infect_rats(self):
        """Процесс заражения"""
        infected_cells = set()
        for x in range(self.n):
            for y in range(self.n):
                for rat_id in self.grid[x][y]:
                    if self.rats_data[rat_id]['status'] == 'I':
                        infected_cells.add((x, y))
        
        for x, y in infected_cells:
            for rat_id in self.grid[x][y]:
                if self.rats_data[rat_id]['status'] == 'S' and random.random() < self.p_infect:
                    self.rats_data[rat_id]['status'] = 'I'
                    self.rats_data[rat_id]['counter'] = 1
    
    def _update_statuses(self):
        """Обновление статусов (болезнь, иммунитет)"""
        for rat_id in self.rats_data:
            status = self.rats_data[rat_id]['status']
            counter = self.rats_data[rat_id]['counter']
            
            if status == 'I':
                if counter >= self.ILL_DAYS:
                    self.rats_data[rat_id]['status'] = 'R'
                    self.rats_data[rat_id]['counter'] = 1
                else:
                    self.rats_data[rat_id]['counter'] += 1
            elif status == 'R':
                if counter >= self.IMMUN_DAYS:
                    self.rats_data[rat_id]['status'] = 'S'
                    self.rats_data[rat_id]['counter'] = 0
                else:
                    self.rats_data[rat_id]['counter'] += 1
    
    def _vaccinate(self, day):
        """Вакцинация в заданный день"""
        if day == self.vacc_day:
            healthy_ids = [rid for rid, d in self.rats_data.items() if d['status'] == 'S']
            target = int(len(healthy_ids) * self.vacc_percent / 100)
            if target > 0 and healthy_ids:
                to_vacc = random.sample(healthy_ids, min(target, len(healthy_ids)))
                for rid in to_vacc:
                    self.rats_data[rid]['status'] = 'R'
                    self.rats_data[rid]['counter'] = 1
    
    def _record_stats(self, week):
        """Запись статистики по неделям"""
        s = sum(1 for d in self.rats_data.values() if d['status'] == 'S')
        i = sum(1 for d in self.rats_data.values() if d['status'] == 'I')
        r = sum(1 for d in self.rats_data.values() if d['status'] == 'R')
        self.history['S'].append(s)
        self.history['I'].append(i)
        self.history['R'].append(r)
        
        if week > 0 and len(self.history['I']) > 1:
            infections_this_week = max(0, i - self.history['I'][week-1] + r - (self.history['R'][week-1] if len(self.history['R']) > 1 else 0))
            self.weekly_infections.append(infections_this_week)
        else:
            self.weekly_infections.append(i)
    
    def _calculate_threshold(self):
        """Расчёт эпидемического порога"""
        if len(self.weekly_infections) >= 8:
            first_8 = self.weekly_infections[:8]
            mean = np.mean(first_8)
            std = np.std(first_8, ddof=1) if len(first_8) > 1 else 0
            threshold = mean + 2.507 * std
            return round(threshold, 1)
        return 0
    
    def _run_single(self, with_vacc=True):
        """Запуск одной симуляции (с вакцинацией или без)"""
        self._init_grid()
        self.history = {'S': [], 'I': [], 'R': []}
        self.weekly_infections = []
        
        total_days = self.weeks * 7
        current_week = 0
        
        for day in range(total_days):
            if with_vacc:
                self._vaccinate(day)
            self._move_rats()
            self._infect_rats()
            self._update_statuses()
            
            if day % 7 == 0:
                self._record_stats(current_week)
                current_week += 1
        
        i_vals = self.history['I']
        peak = max(i_vals) if i_vals else 0
        peak_week = i_vals.index(peak) if peak in i_vals else 0
        return peak, peak_week, self._calculate_threshold()
    
    def _run_comparison(self):
        """Запуск сравнения (с вакцинацией и без)"""
        peak_with, week_with, threshold = self._run_single(with_vacc=True)
        
        peak_without, week_without, _ = self._run_single(with_vacc=False)
        
        self.peaks = {
            'with': peak_with,
            'week_with': week_with,
            'without': peak_without,
            'week_without': week_without
        }
        
        if peak_without > 0:
            self.efficacy = round((peak_without - peak_with) / peak_without * 100, 1)
        else:
            self.efficacy = 0
        
        return threshold
    
    def run(self):
        """Основной метод запуска"""
        threshold = self._run_comparison()
        self.threshold = threshold
        self.matrix_state = self._get_matrix_state()
    
    def _get_matrix_state(self):
        """Получение текущего состояния матрицы для визуализации"""
        matrix = [[{'S': 0, 'I': 0, 'R': 0} for _ in range(self.n)] for _ in range(self.n)]
        for rat_id, data in self.rats_data.items():
            x, y = data['pos']
            status = data['status']
            matrix[x][y][status] += 1
        return matrix
    
    def _get_matrix_display(self):
        """Преобразует matrix_state в список статусов для отображения точек"""
        matrix_display = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                cell = self.matrix_state[i][j]
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
    
    def get_graph(self):
        """Генерация графика в base64"""
        weeks = list(range(len(self.history['S'])))
        plt.figure(figsize=(10, 6))
        plt.plot(weeks, self.history['S'], 'g-', label='S (здоровые)', linewidth=2)
        plt.plot(weeks, self.history['I'], 'r-', label='I (заражённые)', linewidth=2)
        plt.plot(weeks, self.history['R'], 'y-', label='R (иммунные)', linewidth=2)
        plt.axvline(x=self.vacc_day/7, color='purple', linestyle='--', label='Вакцинация')
        plt.xlabel('Недели')
        plt.ylabel('Количество крыс')
        plt.title('Динамика SIR')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{image_base64}"
    
    def get_results(self):
        """Возвращает все результаты для шаблона"""
        return {
            'graph': self.get_graph(),
            'threshold': self.threshold,
            'efficacy': self.efficacy,
            'peak_without': self.peaks['without'],
            'peak_with': self.peaks['with'],
            'week_without': self.peaks['week_without'],
            'week_with': self.peaks['week_with'],
            'matrix_display': self._get_matrix_display(),
            'n': self.n
        }