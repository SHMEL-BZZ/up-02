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

# Импортируем вашу модель 
from model.pp_model import simulate_lotka_volterra, plot_dynamics
from controller.fishing_controller import find_optimal_q

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
    field_errors = {}  # Словарь для ошибок по конкретным полям
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
                    
                    # Генерируем уникальный ID для этой сессии результатов
                    results_id = str(uuid.uuid4())
                    
                    # Сохраняем график в временную папку
                    plot_filename = f"plot_{results_id}.png"
                    plot_dir = os.path.join('static', 'temp_plots')
                    plot_path = os.path.join(plot_dir, plot_filename)
                    
                    # Создаем директорию если её нет
                    os.makedirs(plot_dir, exist_ok=True)
                    
                    # Сохраняем изображение из base64
                    plot_base64_clean = plot_base64
                    if 'base64,' in plot_base64:
                        plot_base64_clean = plot_base64.split('base64,')[1]
                    
                    with open(plot_path, 'wb') as f:
                        f.write(base64.b64decode(plot_base64_clean))
                    
                    # Сохраняем данные в глобальном хранилище
                    temp_results[results_id] = {
                        'x_t': result.prey.tolist() if hasattr(result.prey, 'tolist') else list(result.prey),
                        'y_t': result.predators.tolist() if hasattr(result.predators, 'tolist') else list(result.predators),
                        'time': result.time.tolist() if hasattr(result.time, 'tolist') else list(result.time),
                        'params': {
                            'alpha': alpha,
                            'c': c,
                            'beta': beta,
                            'd': d,
                            'x0': x0,
                            'y0': y0,
                            'T': T,
                            'N': N,
                            'avg_prey': result.avg_prey,
                            'avg_predator': result.avg_predator,
                            'min_prey': min(result.prey),
                            'max_prey': max(result.prey),
                            'min_predator': min(result.predators),
                            'max_predator': max(result.predators)
                        },
                        'plot_path': plot_path
                    }
                    
                    # Формируем результаты для отображения
                    results = {
                        'id': results_id,
                        'plot_id': results_id,
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


@route('/export_csv', method='POST')
def export_csv():
    """Export predator-prey data to CSV file with save dialog"""
    results_id = request.forms.get('results_id', '')
    
    if results_id not in temp_results:
        response.status = 404
        return "Данные не найдены"
    
    data = temp_results[results_id]
    
    # Создаем CSV файл в памяти
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
    writer.writerow(['Среднее', f"{data['params']['avg_prey']:.2f}", f"{data['params']['avg_predator']:.2f}"])
    writer.writerow(['Минимум', f"{data['params']['min_prey']:.2f}", f"{data['params']['min_predator']:.2f}"])
    writer.writerow(['Максимум', f"{data['params']['max_prey']:.2f}", f"{data['params']['max_predator']:.2f}"])
    writer.writerow([])
    
    # Записываем равновесные значения
    writer.writerow(['Равновесные значения'])
    writer.writerow(['Равновесная численность жертв (x*)', f"{data['params']['beta'] / data['params']['d']:.2f}"])
    writer.writerow(['Равновесная численность хищников (y*)', f"{data['params']['alpha'] / data['params']['c']:.2f}"])
    writer.writerow([])
    
    # Записываем временные ряды
    writer.writerow(['Временные ряды'])
    writer.writerow(['Время (лет)', 'Численность жертв', 'Численность хищников'])
    
    for i in range(len(data['time'])):
        writer.writerow([f"{data['time'][i]:.3f}", f"{data['x_t'][i]:.3f}", f"{data['y_t'][i]:.3f}"])
    
    # Генерируем имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"predator_prey_data_{timestamp}.csv"
    
    # Отправляем файл с заголовками для открытия диалога сохранения
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return output.getvalue().encode('utf-8-sig')


@route('/export_plot', method='POST')
def export_plot():
    """Export predator-prey plot to PNG file with save dialog"""
    plot_id = request.forms.get('plot_id', '')
    
    if plot_id not in temp_results:
        response.status = 404
        return "График не найден"
    
    plot_path = temp_results[plot_id]['plot_path']
    
    # Проверяем существует ли файл
    if not os.path.exists(plot_path):
        response.status = 404
        return "Файл графика не найден"
    
    # Читаем файл изображения
    with open(plot_path, 'rb') as f:
        image_data = f.read()
    
    # Генерируем имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"predator_prey_plot_{timestamp}.png"
    
    # Отправляем файл с заголовками для скачивания
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return image_data


@route('/cleanup_temp', method='POST')
def cleanup_temp():
    """Clean up old temporary files"""
    temp_dir = os.path.join('static', 'temp_plots')
    if os.path.exists(temp_dir):
        current_time = datetime.now().timestamp()
        deleted = 0
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath):
                file_time = os.path.getmtime(filepath)
                if current_time - file_time > 3600:  # 1 час
                    os.remove(filepath)
                    deleted += 1
        return f"Очищено {deleted} файлов"
    return "Нет файлов для очистки"


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