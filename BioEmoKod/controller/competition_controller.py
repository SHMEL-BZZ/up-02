"""
Контроллер для модели конкуренции видов
Управление симуляцией и взаимодействие с представлением
"""

from model.competition_model import World, ChartService


class SimulationService:
    """Сервис управления симуляцией"""
    def __init__(self):
        self.world = None
        self.params = None
    
    def init_world(self, n, gray_init, white_init, rye_init,
                   rye_spawn_interval_sec, rye_spawn_count, max_ticks):
        """Инициализация мира с заданными параметрами"""
        self.params = {
            'rye_spawn_interval_sec': rye_spawn_interval_sec,
            'rye_spawn_count': rye_spawn_count,
            'max_ticks': max_ticks
        }
        self.world = World(n, gray_init, white_init, rye_init)
        return self.world.to_dict()
    
    def run_tick(self):
        """Выполнение одного такта"""
        if self.world is None:
            return {'error': 'Мир не инициализирован'}
        
        if self.world.is_simulation_over():
            return {'is_alive': False, 'world': self.world.to_dict(), 'tick': self.world.tick, 'extinct': True}
        
        is_alive = self.world.step(
            self.params['rye_spawn_interval_sec'],
            self.params['rye_spawn_count'],
            self.params['max_ticks']
        )
        return {'is_alive': is_alive, 'world': self.world.to_dict(), 'tick': self.world.tick}
    
    def reset(self):
        """Сброс симуляции"""
        self.world = None
        self.params = None
    
    def export_csv(self):
        """Экспорт истории в CSV"""
        if self.world:
            return self.world.export_csv()
        return None
    
    def get_chart(self):
        """Получение графика"""
        if self.world:
            return ChartService.generate_population_chart(self.world)
        return None
    
    def get_verdict(self):
        """Получение вердикта"""
        if self.world:
            return self.world.get_verdict()
        return "Нет данных"
    
    def get_world_state(self):
        """Получение текущего состояния мира"""
        if self.world:
            return self.world.to_dict()
        return None


def validate_parameters(n, gray_init, white_init, rye_init, 
                        rye_interval, rye_spawn_count, max_ticks):
    """
    Валидация входных параметров симуляции согласно ТЗ
    Возвращает (is_valid, error_message)
    """
    total_cells = n * n
    
    if not (2 <= n <= 10):
        return False, "Размер поля n должен быть в диапазоне от 2 до 10"
    
    if gray_init < 2:
        return False, f"Количество серых крыс должно быть не менее 2 (было {gray_init})"
    if gray_init >= total_cells - 1:
        return False, f"Количество серых крыс не может превышать {total_cells - 2}"
    
    if white_init < 2:
        return False, f"Количество белых крыс должно быть не менее 2 (было {white_init})"
    if white_init >= total_cells - 1:
        return False, f"Количество белых крыс не может превышать {total_cells - 2}"
    
    if gray_init + white_init > total_cells - 1:
        return False, f"Сумма крыс ({gray_init + white_init}) не должна превышать {total_cells - 1}"
    
    if rye_init < 1:
        return False, f"Количество ржи должно быть не менее 1 (было {rye_init})"
    if rye_init > total_cells - 4:
        return False, f"Количество ржи не может превышать {total_cells - 4}"
    
    if not (1 <= rye_interval <= 20):
        return False, "Частота появления ржи должна быть в диапазоне от 1 до 20"
    
    if not (1 <= rye_spawn_count <= 5):
        return False, "Количество новой ржи за раз должно быть в диапазоне от 1 до 5"
    
    if not (1 <= max_ticks <= 200): 
        return False, "Максимум тактов должен быть в диапазоне от 0 до 200"
    
    return True, None


def prepare_display_data(world_state):
    """Подготовка данных для отображения поля"""
    if not world_state:
        return [], []
    
    grid = world_state.get('grid', [])
    if not grid:
        return [], []
    
    n = len(grid)
    
    cell_class = []
    cell_content = []
    
    for i in range(n):
        row_class = []
        row_content = []
        for j in range(n):
            cell = grid[i][j]
            marker = cell.get('marker')
            rats = cell.get('rats', [])
            rye = cell.get('rye', False)
            
            # Приоритет маркеров: битва > мир > смерть
            if marker:
                marker_type = marker.get('type')
                if marker_type == 'fight':
                    if marker.get('species') == 'gray':
                        row_class.append('cell-fight-gray')
                    else:
                        row_class.append('cell-fight-white')
                    row_content.append('⚔️')
                elif marker_type == 'peace':
                    row_class.append('cell-peace')
                    row_content.append('🤝')
                elif marker_type == 'death':
                    row_class.append('cell-death')
                    row_content.append('💀')
                continue
            
            # Крысы
            if rats:
                gray_count = sum(1 for r in rats if r['species'] == 'gray')
                white_count = sum(1 for r in rats if r['species'] == 'white')
                
                if gray_count > 0 and white_count > 0:
                    row_class.append('cell-mixed')
                    row_content.append(f'🐀{gray_count}🐁{white_count}')
                elif gray_count > 0:
                    row_class.append('cell-gray')
                    if gray_count == 1:
                        row_content.append('🐀')
                    else:
                        row_content.append(f'🐀×{gray_count}')
                else:
                    row_class.append('cell-white')
                    if white_count == 1:
                        row_content.append('🐁')
                    else:
                        row_content.append(f'🐁×{white_count}')
                continue
            
            # Рожь
            if rye:
                row_class.append('cell-rye')
                row_content.append('🌾')
                continue
            
            # Пустая клетка
            row_class.append('cell-empty')
            row_content.append('⬜')
        
        cell_class.append(row_class)
        cell_content.append(row_content)
    
    return cell_class, cell_content
