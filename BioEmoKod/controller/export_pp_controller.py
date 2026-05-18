"""
Модуль для экспорта данных модели "Хищник-жертва" в различные форматы
"""

import csv
import json
import os
import base64
import uuid
from datetime import datetime
from io import StringIO, BytesIO
from typing import Dict, Any, Optional
import numpy as np


class ExportManager:
    """Менеджер для управления экспортом данных и временного хранения"""
    
    def __init__(self, temp_dir: str = 'static/temp_plots'):
        """
        Инициализация менеджера экспорта
        
        Параметры:
            temp_dir: директория для временного хранения файлов
        """
        self.temp_dir = temp_dir
        self.temp_results: Dict[str, Dict] = {}
        self._ensure_temp_dir()
    
    def _ensure_temp_dir(self):
        """Создает временную директорию если она не существует"""
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def save_simulation_result(self, result, params: Dict) -> str:
        """
        Сохраняет результаты симуляции во временное хранилище
        
        Параметры:
            result: объект SimulationResult
            params: словарь с параметрами модели
        
        Возвращает:
            unique_id: уникальный идентификатор сохраненных данных
        """
        results_id = str(uuid.uuid4())
        
        # Сохраняем данные в хранилище
        self.temp_results[results_id] = {
            'x_t': result.prey if isinstance(result.prey, list) else result.prey.tolist(),
            'y_t': result.predators if isinstance(result.predators, list) else result.predators.tolist(),
            'time': result.time if isinstance(result.time, list) else result.time.tolist(),
            'params': params,
            'created_at': datetime.now()
        }
        
        return results_id
    
    def save_plot(self, plot_base64: str) -> str:
        """
        Сохраняет график во временный файл
        
        Параметры:
            plot_base64: строка с изображением в base64
        
        Возвращает:
            plot_id: уникальный идентификатор графика
        """
        plot_id = str(uuid.uuid4())
        
        # Очищаем base64 строку
        if 'base64,' in plot_base64:
            plot_base64 = plot_base64.split('base64,')[1]
        
        # Сохраняем файл
        plot_filename = f"plot_{plot_id}.png"
        plot_path = os.path.join(self.temp_dir, plot_filename)
        
        with open(plot_path, 'wb') as f:
            f.write(base64.b64decode(plot_base64))
        
        # Сохраняем информацию о графике
        if plot_id not in self.temp_results:
            self.temp_results[plot_id] = {}
        self.temp_results[plot_id]['plot_path'] = plot_path
        self.temp_results[plot_id]['created_at'] = datetime.now()
        
        return plot_id
    
    def get_data(self, data_id: str) -> Optional[Dict]:
        """Получает данные из хранилища по ID"""
        return self.temp_results.get(data_id)
    
    def get_plot_path(self, plot_id: str) -> Optional[str]:
        """Получает путь к файлу графика"""
        if plot_id in self.temp_results and 'plot_path' in self.temp_results[plot_id]:
            return self.temp_results[plot_id]['plot_path']
        return None
    
    def export_to_csv(self, data_id: str) -> Optional[bytes]:
        """
        Экспортирует данные в CSV формат
        
        Параметры:
            data_id: идентификатор данных
        
        Возвращает:
            bytes: содержимое CSV файла или None если данные не найдены
        """
        data = self.get_data(data_id)
        if not data:
            return None
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Записываем параметры модели
        writer.writerow(['Параметры модели Лотки-Вольтерры'])
        writer.writerow(['Параметр', 'Значение', 'Описание'])
        writer.writerow(['α', data['params']['alpha'], 'Рождаемость жертв'])
        writer.writerow(['c', data['params']['c'], 'Эффективность охоты'])
        writer.writerow(['β', data['params']['beta'], 'Смертность хищников'])
        writer.writerow(['d', data['params']['d'], 'Рост хищников'])
        writer.writerow(['x₀', data['params']['x0'], 'Начальная численность жертв'])
        writer.writerow(['y₀', data['params']['y0'], 'Начальная численность хищников'])
        writer.writerow(['T', data['params']['T'], 'Длительность моделирования (лет)'])
        writer.writerow(['N', data['params']['N'], 'Количество шагов'])
        writer.writerow([])
        
        # Записываем статистику
        writer.writerow(['Статистика'])
        writer.writerow(['Показатель', 'Жертвы', 'Хищники'])
        writer.writerow(['Среднее', f"{data['params'].get('avg_prey', 0):.2f}", 
                        f"{data['params'].get('avg_predator', 0):.2f}"])
        writer.writerow(['Минимум', f"{data['params'].get('min_prey', 0):.2f}", 
                        f"{data['params'].get('min_predator', 0):.2f}"])
        writer.writerow(['Максимум', f"{data['params'].get('max_prey', 0):.2f}", 
                        f"{data['params'].get('max_predator', 0):.2f}"])
        writer.writerow([])
        
        # Записываем равновесные значения
        writer.writerow(['Равновесные значения'])
        writer.writerow(['Равновесная численность жертв (x*)', 
                        f"{data['params'].get('equilibrium_prey', 0):.2f}"])
        writer.writerow(['Равновесная численность хищников (y*)', 
                        f"{data['params'].get('equilibrium_predator', 0):.2f}"])
        writer.writerow([])
        
        # Записываем временные ряды
        writer.writerow(['Временные ряды'])
        writer.writerow(['Время (лет)', 'Численность жертв', 'Численность хищников'])
        
        for i in range(len(data['time'])):
            writer.writerow([
                f"{data['time'][i]:.3f}",
                f"{data['x_t'][i]:.3f}",
                f"{data['y_t'][i]:.3f}"
            ])
        
        return output.getvalue().encode('utf-8-sig')
    
    
    def get_plot_bytes(self, plot_id: str) -> Optional[bytes]:
        """
        Получает байты файла графика
        
        Параметры:
            plot_id: идентификатор графика
        
        Возвращает:
            bytes: содержимое файла графика или None если файл не найден
        """
        plot_path = self.get_plot_path(plot_id)
        if not plot_path or not os.path.exists(plot_path):
            return None
        
        with open(plot_path, 'rb') as f:
            return f.read()
    
    
    def generate_filename(self, prefix: str, extension: str) -> str:
        """
        Генерирует имя файла с временной меткой
        
        Параметры:
            prefix: префикс файла
            extension: расширение файла (без точки)
        
        Возвращает:
            str: сгенерированное имя файла
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"


# Создаем глобальный экземпляр менеджера экспорта
export_manager = ExportManager()


def prepare_export_data(result, form_values: Dict, results_dict: Dict) -> Dict:
    """
    Подготавливает данные для экспорта из результатов симуляции
    
    Параметры:
        result: объект SimulationResult
        form_values: словарь со значениями формы
        results_dict: словарь с результатами для отображения
    
    Возвращает:
        Dict: обновленный словарь результатов с ID для экспорта
    """
    # Подготавливаем параметры для сохранения
    export_params = {
        'alpha': float(form_values.get('alpha', 0)),
        'c': float(form_values.get('c', 0)),
        'beta': float(form_values.get('beta', 0)),
        'd': float(form_values.get('d', 0)),
        'x0': float(form_values.get('x0', 0)),
        'y0': float(form_values.get('y0', 0)),
        'T': float(form_values.get('T', 0)),
        'N': int(form_values.get('N', 0)),
        'avg_prey': float(results_dict.get('avg_prey', 0)),
        'avg_predator': float(results_dict.get('avg_predator', 0)),
        'min_prey': float(results_dict.get('min_prey', 0)),
        'max_prey': float(results_dict.get('max_prey', 0)),
        'min_predator': float(results_dict.get('min_predator', 0)),
        'max_predator': float(results_dict.get('max_predator', 0)),
        'equilibrium_prey': float(results_dict.get('x_star', 0)),
        'equilibrium_predator': float(results_dict.get('y_star', 0)),
        'period': float(results_dict.get('period', 0)),
        'stability_type': results_dict.get('stability_type', '')
    }
    
    # Сохраняем данные симуляции
    results_id = export_manager.save_simulation_result(result, export_params)
    
    # Сохраняем график если есть
    if 'plot_base64' in results_dict:
        plot_id = export_manager.save_plot(results_dict['plot_base64'])
        results_dict['plot_id'] = plot_id
    
    results_dict['id'] = results_id
    
    return results_dict