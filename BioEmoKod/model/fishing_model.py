import random
import matplotlib.pyplot as plt
from collections import defaultdict

class FishLake:
    """Модель популяции рыб в прямоугольном озере N×M."""
    
    def __init__(self, N, M, K, prepro, pdeath, q):
        """
        Параметры:
            N, M — размеры озера 
            K — начальное число рыб 
            prepro — вероятность размножения одной рыбы за шаг
            pdeath — вероятность естественной гибели за шаг
            q — вероятность вылова одной рыбы за шаг
        """
        self.N = N
        self.M = M
        self.prepro = prepro
        self.pdeath = pdeath
        self.q = q
        
        # Сетка озера: 0 — пусто, 1 — рыба
        self.grid = [[0] * M for _ in range(N)]
        all_cells = [(i, j) for i in range(N) for j in range(M)]
        chosen = random.sample(all_cells, min(K, N * M))
        for i, j in chosen:
            self.grid[i][j] = 1
        self.population = len(chosen)
            
    
    def step(self):
        """
        Шаг:
        1) движение
        2) размножение
        3) естественная гибель
        4) промысловый вылов
        Возвращает количество выловленных на этом шагу рыб
        """
        #  1. Движение 
        # Сбор координат всех рыб
        fishes = [(i, j) for i in range(self.N) for j in range(self.M) 
                  if self.grid[i][j] == 1]
        # Случайный порядок
        random.shuffle(fishes)
        
        for r, c in fishes:
            # Возможные ходы: 8 соседей + остаться на месте
            moves = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.N and 0 <= nc < self.M:
                        moves.append((nr, nc))
            moves.append((r, c))   # остаться на месте
            
            # Равновероятный выбор направления
            nr, nc = random.choice(moves)
            
            # Если выбрана другая клетка и она свободна – перемещаемся
            if (nr, nc) != (r, c) and self.grid[nr][nc] == 0:
                self.grid[r][c] = 0
                self.grid[nr][nc] = 1
            # Иначе рыба остаётся на месте
        
        #  2. Размножение 
        #  Собираем всех рыб после движения
        fishes = [(i, j) for i in range(self.N) for j in range(self.M) if self.grid[i][j] == 1]
        random.shuffle(fishes)
        newborns = []   # список клеток, выбранных для потомков
        
        for r, c in fishes:
            if random.random() < self.prepro:
                # Ищем все свободные соседние клетки 
                free_neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.M and self.grid[nr][nc] == 0:
                            free_neighbors.append((nr, nc))
                if free_neighbors:
                    chosen_cell = random.choice(free_neighbors)
                    newborns.append(chosen_cell)
        
        # Добавляем потомков 
        for r, c in set(newborns):
            if self.grid[r][c] == 0:
                self.grid[r][c] = 1
        
        #  3. Естественная гибель 
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 1 and random.random() < self.pdeath:
                    self.grid[i][j] = 0
        
        #  4. Промысловый вылов 
        catch = 0
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 1 and random.random() < self.q:
                    self.grid[i][j] = 0
                    catch += 1
        
        # Обновляем общую численность
        self.population = sum(sum(row) for row in self.grid)
        return catch
    
    def simulate_with_frames(self, total_steps, record_every=1):
        """Возвращает список кадров (сеток) и историю численности."""
        frames = []
        pop_history = [self.population]
        for step in range(total_steps):
            self.step()
            if step % record_every == 0:
                frames.append([row[:] for row in self.grid])
            pop_history.append(self.population)
        return frames, pop_history


