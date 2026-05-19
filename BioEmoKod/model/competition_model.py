"""
Модуль конкуренции видов - модель данных и бизнес-логика
"""

import random
import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Rat:
    """Класс крысы"""
    def __init__(self, species):
        self.species = species
        self.hostility = random.random()
        self.hunger = 0

    
    def to_dict(self):
        """Преобразует состояние крысы в словарь (для сохранения в CSV/JSON)"""
        return {
            'species': self.species,
            'hostility': round(self.hostility, 3),
            'hunger': self.hunger,
        }


class Cell:
    """Класс клетки поля"""
    def __init__(self):
        self.rats = []
        self.rye = False
    
    def to_dict(self):
        """Преобразует состояние клетки в словарь для сохранения"""
        return {
            'rats': [r.to_dict() for r in self.rats],
            'rye': self.rye
        }

class World:
    """Класс мира симуляции"""
    def __init__(self, n, gray, white, rye):
        self.n = n
        self.grid = [[Cell() for _ in range(n)] for _ in range(n)]
        self.gray = 0
        self.white = 0
        self.rye_count = rye
        self.tick = 0
        self.fights = 0
        self.deaths = 0
        self.history = []
        self.is_extinct = False
        self.current_markers = {
            'death_cells': [],
            'fight_cells': [],
            'peace_cells': []
        }
        
        # Размещаем крыс ПАРАМИ в одних клетках
        cells = [(i, j) for i in range(n) for j in range(n)]
        random.shuffle(cells)
        
        cell_idx = 0
        
        # Серые крысы (по 2 в клетку)
        gray_pairs = gray // 2
        gray_remaining = gray % 2
        
        for _ in range(gray_pairs):
            if cell_idx < len(cells):
                x, y = cells[cell_idx]
                rat1 = Rat('gray')
                rat2 = Rat('gray')
                self.grid[x][y].rats.append(rat1)
                self.grid[x][y].rats.append(rat2)
                self.gray += 2
                cell_idx += 1
        
        if gray_remaining and cell_idx < len(cells):
            x, y = cells[cell_idx]
            self.grid[x][y].rats.append(Rat('gray'))
            self.gray += 1
            cell_idx += 1
        
        # Белые крысы (по 2 в клетку)
        white_pairs = white // 2
        white_remaining = white % 2
        
        for _ in range(white_pairs):
            if cell_idx < len(cells):
                x, y = cells[cell_idx]
                rat1 = Rat('white')
                rat2 = Rat('white')
                self.grid[x][y].rats.append(rat1)
                self.grid[x][y].rats.append(rat2)
                self.white += 2
                cell_idx += 1
        
        if white_remaining and cell_idx < len(cells):
            x, y = cells[cell_idx]
            self.grid[x][y].rats.append(Rat('white'))
            self.white += 1
            cell_idx += 1
        
        # Размещение ржи
        rye_placed = 0
        max_attempts = 1000
        attempts = 0
        while rye_placed < rye and attempts < max_attempts:
            x, y = random.randint(0, n-1), random.randint(0, n-1)
            if not self.grid[x][y].rats and not self.grid[x][y].rye:
                self.grid[x][y].rye = True
                rye_placed += 1
            attempts += 1
        
        # Добавляем рожь в клетки с крысами
        self._ensure_rye_with_rats()
        
        self._save_history()
    
    def _ensure_rye_with_rats(self):
        """Добавляет рожь в клетки где есть крысы"""
        cells_with_rats = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].rats and not self.grid[i][j].rye:
                    cells_with_rats.append((i, j))
        
        # Добавляем рожь в клетки с крысами (не более 3)
        for _ in range(min(3, len(cells_with_rats))):
            if cells_with_rats:
                x, y = random.choice(cells_with_rats)
                if not self.grid[x][y].rye:
                    self.grid[x][y].rye = True
                    self.rye_count += 1
                    cells_with_rats.remove((x, y))
