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


def _force_interactions(self):
        """Принудительно создаёт битвы между разными видами"""
        if self.tick == 0 or self.tick % 2 != 0:  # Каждые 2 такта
            return
    
        # Находим клетки с серыми и белыми крысами
        gray_cells = []
        white_cells = []
    
        for i in range(self.n):
            for j in range(self.n):
                cell = self.grid[i][j]
                if cell.rats:
                    if any(r.species == 'gray' for r in cell.rats):
                        gray_cells.append((i, j))
                    if any(r.species == 'white' for r in cell.rats):
                        white_cells.append((i, j))
    
        # Если есть и серые, и белые - создаём битву!
        if gray_cells and white_cells:
            # Берём случайную клетку с серыми
            gx, gy = random.choice(gray_cells)
            # Берём случайную клетку с белыми
            wx, wy = random.choice(white_cells)
        
            # Если это разные клетки - перемещаем белую крысу к серой
            if (gx, gy) != (wx, wy):
                # Находим белую крысу
                white_rat = None
                for rat in self.grid[wx][wy].rats:
                    if rat.species == 'white':
                        white_rat = rat
                        break
            
                # Находим серую крысу (для проверки, но не перемещаем)
                if white_rat and self.grid[gx][gy].rats:
                    # Перемещаем белую крысу в клетку к серым
                    self.grid[wx][wy].rats.remove(white_rat)
                    self.grid[gx][gy].rats.append(white_rat)
                    print(f"FORCED FIGHT: Moved white to ({gx},{gy}) with gray")
        
            # Также пробуем переместить серую к белым для большей вероятности
            if len(gray_cells) > 1 and len(white_cells) > 1:
                gx2, gy2 = gray_cells[1] if len(gray_cells) > 1 else gray_cells[0]
                wx2, wy2 = white_cells[1] if len(white_cells) > 1 else white_cells[0]
            
                if (gx2, gy2) != (wx2, wy2):
                    gray_rat = None
                    for rat in self.grid[gx2][gy2].rats:
                        if rat.species == 'gray':
                            gray_rat = rat
                            break
                
                    if gray_rat and self.grid[wx2][wy2].rats:
                        self.grid[gx2][gy2].rats.remove(gray_rat)
                        self.grid[wx2][wy2].rats.append(gray_rat)
                        print(f"FORCED FIGHT: Moved gray to ({wx2},{wy2}) with white")
    
        # Также добавляем рожь в клетки с несколькими крысами для стимуляции
        for i in range(self.n):
            for j in range(self.n):
                cell = self.grid[i][j]
                if len(cell.rats) >= 2 and not cell.rye:
                    # Добавляем рожь с вероятностью 30%
                    if random.random() < 0.3:
                        cell.rye = True
                        self.rye_count += 1
                        print(f"Added rye to ({i},{j}) for reproduction")
    
def _clear_markers(self):
     """Очистка маркеров текущего такта"""
     self.current_markers = {
        'death_cells': [],
        'fight_cells': [],
        'peace_cells': []
     }
    
def _save_history(self):
    """Сохраняет текущее состояние в историю"""
    self.history.append({
        'tick': self.tick,
        'gray': self.gray,
        'white': self.white,
        'rye': self.rye_count,
        'fights': self.fights,
        'deaths': self.deaths,
        'markers': self.current_markers.copy()
    })
    
def _get_neighbors(self, x, y):
    """Возвращает список соседних клеток"""
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.n and 0 <= ny < self.n:
            neighbors.append((nx, ny))
    return neighbors
    
def _move_rat(self, x, y, rat):
    """Перемещение крысы"""
    neighbors = self._get_neighbors(x, y)
    
    rye_cells = [(nx, ny) for nx, ny in neighbors 
                 if self.grid[nx][ny].rye and not self.grid[nx][ny].rats]
    if rye_cells:
        nx, ny = random.choice(rye_cells)
    else:
        empty_cells = [(nx, ny) for nx, ny in neighbors 
                      if not self.grid[nx][ny].rats and not self.grid[nx][ny].rye]
        if empty_cells:
            nx, ny = random.choice(empty_cells)
        else:
            return x, y
        
    self.grid[x][y].rats.remove(rat)
    self.grid[nx][ny].rats.append(rat)
    return nx, ny

def _process_cell(self, x, y):
        """Обработка взаимодействий в клетке"""
        cell = self.grid[x][y]
        rats = cell.rats

        if len(rats) == 0:
            return

        # Одна крыса: если есть рожь - съедает
        if len(rats) == 1 and cell.rye:
            cell.rye = False
            self.rye_count -= 1
            rats[0].hunger = 0
            return

        # Две или более крысы
        if len(rats) >= 2:
            a, b = rats[0], rats[1]
        
            # Если виды разные - КОНФЛИКТ
            if a.species != b.species:
                hostility_diff = abs(a.hostility - b.hostility)
            
                # МИРНЫЙ РАЗБЕГ
                if hostility_diff < 0.3:
                    self.current_markers['peace_cells'].append((x, y))
                
                    # Разводим крыс по разным клеткам
                    neighbors = self._get_neighbors(x, y)
                    empty_neighbors = [n for n in neighbors if not self.grid[n[0]][n[1]].rats]
                
                    if len(empty_neighbors) >= 2:
                        random.shuffle(empty_neighbors)
                        self.grid[empty_neighbors[0][0]][empty_neighbors[0][1]].rats.append(a)
                        self.grid[empty_neighbors[1][0]][empty_neighbors[1][1]].rats.append(b)
                        rats.remove(a)
                        rats.remove(b)
                    elif len(empty_neighbors) == 1:
                        self.grid[empty_neighbors[0][0]][empty_neighbors[0][1]].rats.append(a)
                        rats.remove(a)
                    return
            
                # ДРАКА
                else:
                    self.fights += 1
                
                    winner = random.choice([a, b])
                    loser = b if winner == a else a
                
                    # Добавляем маркер битвы
                    self.current_markers['fight_cells'].append((x, y, winner.species))
                
                    # Удаляем проигравшего
                    rats.remove(loser)
                    self.deaths += 1
                    self.current_markers['death_cells'].append((x, y, loser.species))
                
                    if loser.species == 'gray':
                        self.gray -= 1
                    else:
                        self.white -= 1
                
                    # Победитель съедает рожь
                    if cell.rye:
                        cell.rye = False
                        self.rye_count -= 1
                        winner.hunger = 0
                
                    return
        
            # Если виды одинаковые - РАСХОДЯТСЯ МИРНО
            else:
                self.current_markers['peace_cells'].append((x, y))
            
                # Разводим крыс по разным клеткам
                neighbors = self._get_neighbors(x, y)
                empty_neighbors = [n for n in neighbors if not self.grid[n[0]][n[1]].rats]
            
                if len(empty_neighbors) >= 2:
                    random.shuffle(empty_neighbors)
                    self.grid[empty_neighbors[0][0]][empty_neighbors[0][1]].rats.append(a)
                    self.grid[empty_neighbors[1][0]][empty_neighbors[1][1]].rats.append(b)
                    rats.remove(a)
                    rats.remove(b)
                elif len(empty_neighbors) == 1:
                    self.grid[empty_neighbors[0][0]][empty_neighbors[0][1]].rats.append(a)
                    rats.remove(a)
                # Если нет свободных клеток - обе остаются на месте
                return


def _force_interactions(self):
        """Принудительно создаёт конфликты между разными видами"""
        if self.tick == 0 or self.tick % 2 != 0:  # Каждые 2 такта
            return
    
        # Находим клетки с серыми и белыми крысами
        gray_cells = []
        white_cells = []
    
        for i in range(self.n):
            for j in range(self.n):
                cell = self.grid[i][j]
                if cell.rats:
                    if any(r.species == 'gray' for r in cell.rats):
                        gray_cells.append((i, j))
                    if any(r.species == 'white' for r in cell.rats):
                        white_cells.append((i, j))
    
        # Создаём битву: перемещаем крысу одного вида в клетку с другим видом
        if gray_cells and white_cells:
            # Берём случайную клетку с серыми
            gx, gy = random.choice(gray_cells)
            # Берём случайную клетку с белыми
            wx, wy = random.choice(white_cells)
        
            # Если это разные клетки - перемещаем белую крысу к серой
            if (gx, gy) != (wx, wy):
                # Находим белую крысу
                white_rat = None
                for rat in self.grid[wx][wy].rats:
                    if rat.species == 'white':
                        white_rat = rat
                        break
            
                if white_rat:
                    # Перемещаем белую крысу в клетку к серым
                    self.grid[wx][wy].rats.remove(white_rat)
                    self.grid[gx][gy].rats.append(white_rat)
        
            # Также пробуем переместить серую к белым для большей вероятности
            if len(gray_cells) > 1 and len(white_cells) > 1:
                gx2, gy2 = gray_cells[1] if len(gray_cells) > 1 else gray_cells[0]
                wx2, wy2 = white_cells[1] if len(white_cells) > 1 else white_cells[0]
            
                if (gx2, gy2) != (wx2, wy2):
                    gray_rat = None
                    for rat in self.grid[gx2][gy2].rats:
                        if rat.species == 'gray':
                            gray_rat = rat
                            break
                
                    if gray_rat:
                        self.grid[gx2][gy2].rats.remove(gray_rat)
                        self.grid[wx2][wy2].rats.append(gray_rat)   

def _apply_hunger(self):
        """Применение голода"""
        for i in range(self.n):
            for j in range(self.n):
                cell = self.grid[i][j]
                for rat in cell.rats[:]:
                    rat.hunger += 1
                    if rat.hunger >= 10:
                        cell.rats.remove(rat)
                        self.deaths += 1
                        self.current_markers['death_cells'].append((i, j, rat.species))
                        if rat.species == 'gray':
                            self.gray -= 1
                        else:
                            self.white -= 1
    
def _spawn_rye(self, interval, count):
        """Появление новой ржи"""
        if self.tick > 0 and self.tick % max(1, interval) == 0:
            empty = [(i, j) for i in range(self.n) for j in range(self.n)
                    if not self.grid[i][j].rats and not self.grid[i][j].rye]
            
            for _ in range(min(count, len(empty))):
                if empty:
                    x, y = random.choice(empty)
                    self.grid[x][y].rye = True
                    self.rye_count += 1
                    empty.remove((x, y))
    
def _reset_flags(self):
        """Сброс флагов крыс"""
        for i in range(self.n):
            for j in range(self.n):
                for rat in self.grid[i][j].rats:
                    rat.reset_flags()
    
def is_simulation_over(self):
        """Проверка окончания симуляции"""
        if self.gray == 0 or self.white == 0:
            self.is_extinct = True
            return True
        return False
    
def step(self, interval, count, max_ticks):
        """Выполнение одного такта симуляции"""
        if self.is_simulation_over():
            return False
    
        if self.tick >= max_ticks:
            return False
    
        self.tick += 1
        self._clear_markers()
    
        # 1. Перемещение крыс
        for i in range(self.n):
            for j in range(self.n):
                for rat in self.grid[i][j].rats[:]:
                    self._move_rat(i, j, rat)
    
        # 2. Принудительные взаимодействия (создаём битвы)
        self._force_interactions()
    
        # 3. Взаимодействия в клетках (битвы и размножение)
        for i in range(self.n):
            for j in range(self.n):
                self._process_cell(i, j)
    
        # 4. Применение голода
        self._apply_hunger()
    
        # 5. Появление новой ржи
        self._spawn_rye(interval, count)
    
        # 6. Добавляем рожь если её мало
        if self.rye_count < 3 and self.tick % 3 == 0:
            empty_cells = [(i, j) for i in range(self.n) for j in range(self.n)
                          if not self.grid[i][j].rats and not self.grid[i][j].rye]
            for _ in range(min(2, len(empty_cells))):
                if empty_cells:
                    x, y = random.choice(empty_cells)
                    self.grid[x][y].rye = True
                    self.rye_count += 1
                    empty_cells.remove((x, y))
    
    
        self._save_history()
        return True