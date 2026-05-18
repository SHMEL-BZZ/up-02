"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, response
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt
import random
import uuid
import os
import base64
import json
import csv
from io import StringIO

# Импортируем модель
from model.pp_model import simulate_lotka_volterra, plot_dynamics
from controller.fishing_controller import find_optimal_q
# Импортируем менеджер экспорта
from controller.export_pp_controller import export_manager, prepare_export_data


# Создаем глобальное хранилище для временных результатов
temp_results = {}

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )


@route('/predator_pray', method=['GET', 'POST'])
def predator_pray():
    """Renders the predator_pray page and handles form submission."""
    title = 'Модель «Хищник-жертва»'
    results = None
    error = None
    field_errors = {}
    form_values = {}
    
    # Значения по умолчанию
    default_form_values = {
        'x0': '50', 'y0': '20', 'alpha': '0.8', 'c': '0.04',
        'beta': '0.6', 'd': '0.02', 'T': '50', 'N': '1000'
    }
    
    if request.method == 'POST':
        # Сброс формы
        if request.forms.get('reset') == 'true':
            form_values = default_form_values.copy()
            field_errors = {}
        elif request.forms.get('random') == 'true':
            form_values = generate_random_values()
            field_errors = {}
            # Автоматически запускаем расчёт со сгенерированными значениями
            # Преобразуем строки в числа для расчёта
            x0 = float(form_values['x0'])
            y0 = float(form_values['y0'])
            alpha = float(form_values['alpha'])
            c = float(form_values['c'])
            beta = float(form_values['beta'])
            d = float(form_values['d'])
            T = float(form_values['T'])
            N = int(form_values['N'])
        else:
            # Получаем значения из формы
            form_values = {
                'x0': request.forms.get('x0', '').strip(),
                'y0': request.forms.get('y0', '').strip(),
                'alpha': request.forms.get('alpha', '').strip(),
                'c': request.forms.get('c', '').strip(),
                'beta': request.forms.get('beta', '').strip(),
                'd': request.forms.get('d', '').strip(),
                'T': request.forms.get('T', '').strip(),
                'N': request.forms.get('N', '').strip()
            }
            
            # Инициализируем переменные со значениями по умолчанию
            x0 = y0 = alpha = c = beta = d = T = None
            N = None
            
            # Функция для преобразования в float (с поддержкой запятой)
            def to_float(value, field_name, errors, required=True):
                if not value and required:
                    errors[field_name] = 'Поле обязательно для заполнения'
                    return None
                if value:
                    try:
                        # Заменяем запятую на точку
                        value = value.replace(',', '.')
                        return float(value)
                    except (ValueError, TypeError):
                        errors[field_name] = f'Некорректное число: {value}'
                        return None
                return None
            
            # Функция для преобразования в int
            def to_int(value, field_name, errors, required=True):
                if not value and required:
                    errors[field_name] = 'Поле обязательно для заполнения'
                    return None
                if value:
                    try:
                        value = value.replace(',', '.')
                        return int(float(value))
                    except (ValueError, TypeError):
                        errors[field_name] = f'Некорректное целое число: {value}'
                        return None
                return None
            
            # Преобразуем все значения
            x0 = to_float(form_values['x0'], 'x0', field_errors)
            y0 = to_float(form_values['y0'], 'y0', field_errors)
            alpha = to_float(form_values['alpha'], 'alpha', field_errors)
            c = to_float(form_values['c'], 'c', field_errors)
            beta = to_float(form_values['beta'], 'beta', field_errors)
            d = to_float(form_values['d'], 'd', field_errors)
            T = to_float(form_values['T'], 'T', field_errors)
            N = to_int(form_values['N'], 'N', field_errors)
            
            # Валидация диапазонов (только если поле не пустое и нет ошибок преобразования)
            if x0 is not None and 'x0' not in field_errors and not (10 <= x0 <= 100):
                field_errors['x0'] = 'Число жертв должно быть в диапазоне 10–100'
            if y0 is not None and 'y0' not in field_errors and not (1 <= y0 <= 50):
                field_errors['y0'] = 'Число хищников должно быть в диапазоне 1–50'
            if T is not None and 'T' not in field_errors and not (5 <= T <= 50):
                field_errors['T'] = 'Длительность должна быть в диапазоне 5–50 лет'
            if N is not None and 'N' not in field_errors and not (200 <= N <= 10000):
                field_errors['N'] = 'Число шагов должно быть в диапазоне 200–10000'
            if alpha is not None and 'alpha' not in field_errors and not (0.4 <= alpha <= 1.5):
                field_errors['alpha'] = 'Рождаемость жертв должна быть в диапазоне 0.4–1.5'
            if c is not None and 'c' not in field_errors and not (0.01 <= c <= 0.06):
                field_errors['c'] = 'Эффективность охоты должна быть в диапазоне 0.01–0.06'
            if beta is not None and 'beta' not in field_errors and not (0.4 <= beta <= 1.5):
                field_errors['beta'] = 'Смертность хищников должна быть в диапазоне 0.4–1.5'
            if d is not None and 'd' not in field_errors and not (0.01 <= d <= 0.06):
                field_errors['d'] = 'Рост хищников должен быть в диапазоне 0.01–0.06'
            
            # Если есть ошибки - показываем их без расчёта
            if field_errors:
                error = "Пожалуйста, исправьте ошибки в форме"

            else:
                # Все проверки пройдены, выполняем расчёт
                try:
                    result = simulate_lotka_volterra(
                        x0=x0, y0=y0,
                        alpha=alpha, c=c,
                        beta=beta, d=d,
                        T=T, N=N
                    )
                    
                    plot_base64 = plot_dynamics(result)
                    
                    # Формируем результаты для отображения
                    results = {
                        'x_star': f"{result.equilibrium_prey:.2f}",
                        'y_star': f"{result.equilibrium_predator:.2f}",
                        'period': f"{result.period:.2f}",
                        'stability_type': result.stability_type,
                        'avg_prey': f"{result.avg_prey:.2f}",
                        'avg_predator': f"{result.avg_predator:.2f}",
                        'min_prey': f"{min(result.prey):.2f}",
                        'max_prey': f"{max(result.prey):.2f}",
                        'min_predator': f"{min(result.predators):.2f}",
                        'max_predator': f"{max(result.predators):.2f}",
                        'plot_base64': plot_base64
                    }
                    
                    # Подготавливаем данные для экспорта
                    from controller.export_pp_controller import prepare_export_data
                    results = prepare_export_data(result, form_values, results)
                    
                except Exception as e:
                    error = f"Ошибка расчёта: {str(e)}"
    else:
        # GET запрос - устанавливаем значения по умолчанию
        form_values = default_form_values.copy()
    
    return template('predator_pray', 
                   title=title, 
                   year=datetime.now().year,
                   results=results,
                   error=error,
                   form_values=form_values,
                   field_errors=field_errors)

def generate_random_values():
    """Генерирует случайные значения в допустимых диапазонах"""
    return {
        'x0': str(random.randint(10, 100)),           # жертвы 10-100
        'y0': str(random.randint(1, 50)),             # хищники 1-50
        'alpha': f"{random.uniform(0.4, 1.5):.2f}",   # рождаемость жертв 0.4-1.5
        'c': f"{random.uniform(0.01, 0.06):.3f}",     # эффективность охоты 0.01-0.06
        'beta': f"{random.uniform(0.4, 1.5):.2f}",    # смертность хищников 0.4-1.5
        'd': f"{random.uniform(0.01, 0.06):.3f}",     # рост хищников 0.01-0.06
        'T': str(random.randint(5, 50)),              # длительность 5-50
        'N': str(random.randint(200, 10000))          # шаги 200-10000
    }

@route('/export_csv', method='POST')
def export_csv():
    """Export predator-prey data to CSV file with save dialog"""
    results_id = request.forms.get('results_id', '')
    
    csv_data = export_manager.export_to_csv(results_id)
    if csv_data is None:
        response.status = 404
        return "Данные не найдены"
    
    filename = export_manager.generate_filename('predator_prey_data', 'csv')
    
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return csv_data


@route('/export_plot', method='POST')
def export_plot():
    """Export predator-prey plot to PNG file with save dialog"""
    plot_id = request.forms.get('plot_id', '')
    
    plot_bytes = export_manager.get_plot_bytes(plot_id)
    if plot_bytes is None:
        response.status = 404
        return "График не найден"
    
    filename = export_manager.generate_filename('predator_prey_plot', 'png')
    
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return plot_bytes





from model.epidemic import EpidemicSimulation

@route('/epidemic', method=['GET', 'POST'])
def epidemic():
    """Renders the epidemic page and handles form submission."""
    title = 'Модель «Распространение эпидемии»'
    results = None
    error = None
    field_errors = {}
    form_values = {}
    
    # Значения по умолчанию
    default_form_values = {
        'grid_size': '8',
        'total_rats': '64',
        'weeks': '52',
        'p_infect': '0.6',
        'p_move': '0.5',
        'vacc_day': '56',
        'vacc_percent': '50'
    }
    
    if request.method == 'POST':
        # Сброс формы
        if request.forms.get('reset') == 'true':
            form_values = default_form_values.copy()
            field_errors = {}
        else:
            # Получаем значения из формы
            form_values = {
                'grid_size': request.forms.get('grid_size', '').strip(),
                'total_rats': request.forms.get('total_rats', '').strip(),
                'weeks': request.forms.get('weeks', '').strip(),
                'p_infect': request.forms.get('p_infect', '').strip(),
                'p_move': request.forms.get('p_move', '').strip(),
                'vacc_day': request.forms.get('vacc_day', '').strip(),
                'vacc_percent': request.forms.get('vacc_percent', '').strip()
            }
            
            # Функция для преобразования в float (с поддержкой запятой)
            def to_float(value, field_name, errors, required=True):
                if not value and required:
                    errors[field_name] = 'Поле обязательно для заполнения'
                    return None
                if value:
                    try:
                        # Заменяем запятую на точку
                        value = value.replace(',', '.')
                        return float(value)
                    except (ValueError, TypeError):
                        errors[field_name] = f'Некорректное число: {value}'
                        return None
                return None
            
            # Функция для преобразования в int
            def to_int(value, field_name, errors, required=True):
                if not value and required:
                    errors[field_name] = 'Поле обязательно для заполнения'
                    return None
                if value:
                    try:
                        value = value.replace(',', '.')
                        return int(float(value))
                    except (ValueError, TypeError):
                        errors[field_name] = f'Некорректное целое число: {value}'
                        return None
                return None
            
            # Преобразуем все значения
            grid_size = to_int(form_values['grid_size'], 'grid_size', field_errors)
            total_rats = to_int(form_values['total_rats'], 'total_rats', field_errors)
            weeks = to_int(form_values['weeks'], 'weeks', field_errors)
            p_infect = to_float(form_values['p_infect'], 'p_infect', field_errors)
            p_move = to_float(form_values['p_move'], 'p_move', field_errors)
            vacc_day = to_int(form_values['vacc_day'], 'vacc_day', field_errors)
            vacc_percent = to_int(form_values['vacc_percent'], 'vacc_percent', field_errors)
            
            # Валидация диапазонов (только если поле не пустое и нет ошибок преобразования)
            if grid_size is not None and 'grid_size' not in field_errors and not (2 <= grid_size <= 15):
                field_errors['grid_size'] = 'Размер сетки должен быть в диапазоне 2–15'
            
            # Максимальное количество крыс = n² × 4
            if grid_size is not None and total_rats is not None and 'total_rats' not in field_errors:
                max_rats = grid_size * grid_size * 4
                if not (1 <= total_rats <= max_rats):
                    field_errors['total_rats'] = f'Число крыс должно быть в диапазоне 1–{max_rats} (максимум n² × 4)'
            elif total_rats is not None and 'total_rats' not in field_errors and not (1 <= total_rats <= 400):
                field_errors['total_rats'] = 'Число крыс должно быть в диапазоне 1–400'
            
            if weeks is not None and 'weeks' not in field_errors and not (10 <= weeks <= 520):
                field_errors['weeks'] = 'Длительность должна быть в диапазоне 10–520 недель'
            
            if p_infect is not None and 'p_infect' not in field_errors and not (0.1 <= p_infect <= 1.0):
                field_errors['p_infect'] = 'Вероятность заражения должна быть в диапазоне 0.1–1.0'
            
            if p_move is not None and 'p_move' not in field_errors and not (0.1 <= p_move <= 0.9):
                field_errors['p_move'] = 'Вероятность перемещения должна быть в диапазоне 0.1–0.9'
            
            # День вакцинации должен быть не меньше 7 и не больше общего количества дней
            if vacc_day is not None and weeks is not None and 'vacc_day' not in field_errors:
                max_day = weeks * 7
                if not (7 <= vacc_day <= max_day):
                    field_errors['vacc_day'] = f'День вакцинации должен быть в диапазоне 7–{max_day} (дней симуляции)'
            elif vacc_day is not None and 'vacc_day' not in field_errors and not (7 <= vacc_day <= 3640):
                field_errors['vacc_day'] = 'День вакцинации должен быть не меньше 7'
            
            if vacc_percent is not None and 'vacc_percent' not in field_errors and not (1 <= vacc_percent <= 100):
                field_errors['vacc_percent'] = 'Процент вакцинации должен быть в диапазоне 1–100%'
            
            # Если есть ошибки - показываем их без расчёта
            if field_errors:
                error = "Пожалуйста, исправьте ошибки в форме"
            else:
                # Все проверки пройдены, выполняем расчёт
                try:
                    params = {
                        'grid_size': grid_size,
                        'total_rats': total_rats,
                        'weeks': weeks,
                        'p_infect': p_infect,
                        'p_move': p_move,
                        'vacc_day': vacc_day,
                        'vacc_percent': vacc_percent
                    }
                    sim = EpidemicSimulation(params)
                    sim_results = sim.get_results()
                    
                    # Вычисляем снижение пика
                    peak_without = sim_results['peak_without']
                    peak_with = sim_results['peak_with']
                    reduction = round((peak_without - peak_with) / peak_without * 100, 1) if peak_without > 0 else 0
                    
                    # Формируем результаты
                    results = {
                        'graph': sim_results['graph'],
                        'threshold': sim_results['threshold'],
                        'efficacy': sim_results['efficacy'],
                        'peak_without': peak_without,
                        'peak_with': peak_with,
                        'week_without': sim_results['week_without'],
                        'week_with': sim_results['week_with'],
                        'reduction': reduction,
                        'matrix_display': sim_results['matrix_display'],
                        'n': sim_results['n']
                    }
                except Exception as e:
                    error = f"Ошибка расчёта: {str(e)}"
    else:
        # GET запрос - устанавливаем значения по умолчанию
        form_values = default_form_values.copy()
    
    return template('epidemic', 
                   title=title, 
                   year=datetime.now().year,
                   results=results,
                   error=error,
                   form_values=form_values,
                   field_errors=field_errors)

@route('/competition')
@view('competition')
def competition():
    """Renders the competition page."""
    return dict(
        title='Competition',
        year=datetime.now().year
    )


@route('/fishing', method=['GET', 'POST'])
def fishing():
    title = 'Динамика рыбного промысла'
    results = None
    error = None
    field_errors = {}
    form_values = {}
    
    default_form_values = {
        'N': '15',
        'M': '15',
        'K': '50',
        'p_repro': '0.25',
        'p_death': '0.1'
    }
    
    if request.method == 'POST':
        if request.forms.get('reset') == 'true':
            form_values = default_form_values.copy()
            field_errors = {}
        else:
            # Получаем параметры из формы
            form_values = {
                'N': request.forms.get('N', '').strip(),
                'M': request.forms.get('M', '').strip(),
                'K': request.forms.get('K', '').strip(),
                'p_repro': request.forms.get('p_repro', '').strip(),
                'p_death': request.forms.get('p_death', '').strip()
            }
            
            # Проверка обязательных полей
            for field in ['N', 'M', 'K', 'p_repro', 'p_death']:
                if not form_values[field]:
                    field_errors[field] = 'Поле обязательно для заполнения'
            
            if not field_errors:
                try:
                    # Преобразование в числа
                    N = int(form_values['N'])
                    M = int(form_values['M'])
                    K = int(form_values['K'])
                    p_repro = float(form_values['p_repro'].replace(',', '.'))
                    p_death = float(form_values['p_death'].replace(',', '.'))
                    
                    # Валидация
                    if not (1 <= N <= 50):
                        field_errors['N'] = "Размер популяции N должен быть в диапазоне 1–50"
                    if not (1 <= M <= 50):
                        field_errors['M'] = "Размер популяции M должен быть в диапазоне 1–50"
                    if not (10 <= K <= 200):
                        field_errors['K'] = "Емкость среды K должна быть в диапазоне 10–200"
                    if not (0.1 <= p_repro <= 0.5):
                        field_errors['p_repro'] = "Вероятность размножения должна быть в диапазоне 0.1–0.5"
                    if not (0.05 <= p_death <= 0.3):
                        field_errors['p_death'] = "Вероятность смерти должна быть в диапазоне 0.05–0.3"
                    
                    if field_errors:
                        error = "Пожалуйста, исправьте ошибки в форме"
                    else:
                        # Вызов оптимизации 
                        results_raw, q_opt = find_optimal_q(
                            N, M, K, p_repro, p_death,
                            steps_warmup=300,
                            steps_eval=300,
                            trials=3
                        )
                        
                        # Преобразование результатов для удобства отображения
                        q_vals = sorted(results_raw.keys())
                        catches = [results_raw[q][0] for q in q_vals]
                        pops = [results_raw[q][1] for q in q_vals]
                        
                        results = {
                            'q_vals': q_vals,
                            'catches': catches,
                            'pops': pops,
                            'q_opt': q_opt
                        }
                    
                except ValueError as e:
                    field_errors['general'] = f"Ошибка преобразования данных: {str(e)}"
                    error = "Пожалуйста, исправьте ошибки в форме"
                except Exception as e:
                    error = f"Ошибка расчёта: {str(e)}"
    else:
        form_values = default_form_values.copy()
    
    return template('fishing',
                   title=title,
                   year=datetime.now().year,
                   results=results,
                   error=error,
                   form_values=form_values,
                   field_errors=field_errors)


@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        year=datetime.now().year
    )