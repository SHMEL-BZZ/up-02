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
        
        # Случайное равномерное размещение K рыб без повторений
        all_cells = [(i, j) for i in range(N) for j in range(M)]
        chosen = random.sample(all_cells, K)
        for i, j in chosen:
            self.grid[i][j] = 1
            
        self.population = K   # текущая численность
    
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
        current_fishes = [(i, j) for i in range(self.N) for j in range(self.M) 
                          if self.grid[i][j] == 1]
        random.shuffle(current_fishes)  
        newborns = []   # список клеток, выбранных для потомков
        
        for r, c in current_fishes:
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
        for cell in set(newborns):
            r, c = cell
            if self.grid[r][c] == 0:
                self.grid[r][c] = 1
        
        #  3. Естественная гибель 
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 1:
                    if random.random() < self.pdeath:
                        self.grid[i][j] = 0
        
        #  4. Промысловый вылов 
        catch = 0
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 1:
                    if random.random() < self.q:
                        self.grid[i][j] = 0
                        catch += 1
        
        # Обновляем общую численность
        self.population = sum(sum(row) for row in self.grid)
        return catch
    
    def simulate(self, T):
        """
        Запуск модели на T шагов.
        Возвращает:
            pop_history  — список численности (начальная + после каждого шага)
            catch_history — список уловов на каждом шаге
        """
        pop_history = [self.population]
        catch_history = []
        for _ in range(T):
            catch = self.step()
            pop_history.append(self.population)
            catch_history.append(catch)
        return pop_history, catch_history


