"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, response, static_file
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt
import random
import csv
import io

# Импортир модели "Хищник-жертва" 
from model.pp_model import simulate_lotka_volterra, plot_dynamics
from controller.fishing_controller import find_optimal_q

# Импорт модели "Развитие эпидемии"
from model.epidemic import SimulationResult
from controller.epidemic_controller import plot_epidemic_dynamics, plot_comparison_chart, analyze_epidemic_scenario

# Обработчик статических файлов
@route('/static/<filepath:path>')
def server_static(filepath):
    """Serve static files."""
    return static_file(filepath, root='static/')

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

@route('/epidemic', method=['GET', 'POST'])
def epidemic():
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
        # Генерация случайных значений
        if request.forms.get('random') == 'true':
            import random
            # Генерируем случайные значения с учётом зависимостей
            grid_size = random.randint(2, 10)
            max_rats = grid_size * grid_size * 4
            total_rats = random.randint(2, max_rats)
            weeks = random.randint(8, 260)
            p_infect = round(random.uniform(0.1, 0.9), 1)
            p_move = round(random.uniform(0.1, 0.9), 1)
            max_vacc_day = weeks * 7
            vacc_day = random.randint(56, max_vacc_day)
            vacc_percent = random.randint(1, 100)
            
            form_values = {
                'grid_size': str(grid_size),
                'total_rats': str(total_rats),
                'weeks': str(weeks),
                'p_infect': str(p_infect),
                'p_move': str(p_move),
                'vacc_day': str(vacc_day),
                'vacc_percent': str(vacc_percent)
            }
            field_errors = {}

            # Выполняем расчёт для сгенерированных значений
            try:
                analysis = analyze_epidemic_scenario(
                    n=grid_size,
                    total_rats=total_rats,
                    weeks=weeks,
                    p_infect=p_infect,
                    p_move=p_move,
                    vacc_day=vacc_day,
                    vacc_percent=vacc_percent,
                )
                
                results = {
                    'graph': analysis['graph'],
                    'threshold': analysis['results']['Эпидемический порог'],
                    'efficacy': float(analysis['evaluation']['Эффективность вакцинации'].rstrip('%')),
                    'peak_without': analysis['results']['Пик заражения (без вакцинации)'],
                    'peak_with': analysis['results']['Пик заражения (с вакцинацией)'],
                    'week_without': analysis['results']['Неделя пика (без вакцинации)'],
                    'week_with': analysis['results']['Неделя пика (с вакцинацией)'],
                    'matrix_display': analysis['simulation_result'].matrix_display,
                    'n': analysis['simulation_result'].n,
                    'epidemic_weeks_without': analysis['results']['Эпидемические недели (без вакцинации)'],
                    'epidemic_weeks_with': analysis['results']['Эпидемические недели (с вакцинацией)'],
                    'history_matrices': analysis['simulation_result'].history_matrices,
                    'total_days': analysis['simulation_result'].total_days
                }
            except Exception as e:
                error = f"Ошибка расчёта: {str(e)}"
                import traceback
                traceback.print_exc()

        # Сброс формы
        elif request.forms.get('reset') == 'true':
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
            
            # Функция для преобразования в int с валидацией
            def to_int(value, field_name, errors, required=True):
                if not value and required:
                    errors[field_name] = 'Поле обязательно для заполнения'
                    return None
                if value:
                    # Проверка на отрицательные числа и буквы в начале
                    value = value.strip()
                    if value.startswith('-'):
                        errors[field_name] = 'Значение не может быть отрицательным'
                        return None
                    
                    # Проверка на буквы и другие символы
                    import re
                    if not re.match(r'^[\d]+$', value.replace(',', '').replace('.', '')):
                        errors[field_name] = 'Значение должно быть целым положительным числом'
                        return None
                    
                    try:
                        # Заменяем запятую на точку и преобразуем
                        value = value.replace(',', '.')
                        # Проверяем, что после преобразования нет дробной части
                        float_val = float(value)
                        if float_val != int(float_val):
                            errors[field_name] = 'Значение должно быть целым числом (без дробной части)'
                            return None
                        int_val = int(float_val)
                        if int_val < 0:
                            errors[field_name] = 'Значение не может быть отрицательным'
                            return None
                        return int_val
                    except (ValueError, TypeError):
                        errors[field_name] = 'Некорректное число'
                        return None
                return None

            # 1. Валидация размера сетки (2-10)
            grid_size = to_int(form_values['grid_size'], 'grid_size', field_errors)
            if grid_size is not None and 'grid_size' not in field_errors:
                if not (2 <= grid_size <= 10):
                    field_errors['grid_size'] = 'Размер сетки должен быть в диапазоне от 2 до 10'
            
            # 2. Валидация количества крыс (2 до n*n*4)
            total_rats = to_int(form_values['total_rats'], 'total_rats', field_errors)
            if total_rats is not None and 'total_rats' not in field_errors:
                if grid_size is not None and 'grid_size' not in field_errors:
                    max_rats = grid_size * grid_size * 4
                    if not (2 <= total_rats <= max_rats):
                        field_errors['total_rats'] = f'Число крыс должно быть в диапазоне от 2 до {max_rats} (при размере сетки {grid_size}x{grid_size})'
            
            # 3. Валидация длительности в неделях (8-260)
            weeks = to_int(form_values['weeks'], 'weeks', field_errors)
            if weeks is not None and 'weeks' not in field_errors:
                if not (8 <= weeks <= 260):
                    field_errors['weeks'] = 'Длительность должна быть в диапазоне от 8 до 260 недель'
            
            # 4. Валидация вероятности заражения (0.1-0.9, 2 знака)
            p_infect = to_float(form_values['p_infect'], 'p_infect', field_errors)
            if p_infect is not None and 'p_infect' not in field_errors:
                if not (0.1 <= p_infect <= 0.9):
                    field_errors['p_infect'] = 'Вероятность заражения должна быть в диапазоне от 0.1 до 0.9'
            
            # 5. Валидация вероятности перемещения (0.1-0.9, 2 знака)
            p_move = to_float(form_values['p_move'], 'p_move', field_errors)
            if p_move is not None and 'p_move' not in field_errors:
                if not (0.1 <= p_move <= 0.9):
                    field_errors['p_move'] = 'Вероятность перемещения должна быть в диапазоне от 0.1 до 0.9'
            
            # 6. Валидация дня начала вакцинации (56 - weeks*7)
            vacc_day = to_int(form_values['vacc_day'], 'vacc_day', field_errors)
            if vacc_day is not None and 'vacc_day' not in field_errors:
                if weeks is not None and 'weeks' not in field_errors:
                    max_day = weeks * 7
                    min_day = 56
                    if not (min_day <= vacc_day <= max_day):
                        field_errors['vacc_day'] = f'День начала вакцинации должен быть в диапазоне от {min_day} до {max_day} дней (с 8-й недели до конца симуляции)'
                else:
                    # Если недели еще не валидированы, но день вакцинации задан
                    if not (1 <= vacc_day <= 1820):  # 260 * 7
                        field_errors['vacc_day'] = 'День вакцинации должен быть положительным числом'
            
            # 7. Валидация процента вакцинируемых крыс (1-100)
            vacc_percent = to_int(form_values['vacc_percent'], 'vacc_percent', field_errors)
            if vacc_percent is not None and 'vacc_percent' not in field_errors:
                if not (1 <= vacc_percent <= 100):
                    field_errors['vacc_percent'] = 'Процент вакцинации должен быть в диапазоне от 1 до 100%'

            # Преобразуем все значения
            grid_size = to_int(form_values['grid_size'], 'grid_size', field_errors)
            total_rats = to_int(form_values['total_rats'], 'total_rats', field_errors)
            weeks = to_int(form_values['weeks'], 'weeks', field_errors)
            p_infect = to_float(form_values['p_infect'], 'p_infect', field_errors)
            p_move = to_float(form_values['p_move'], 'p_move', field_errors)
            vacc_day = to_int(form_values['vacc_day'], 'vacc_day', field_errors)
            vacc_percent = to_int(form_values['vacc_percent'], 'vacc_percent', field_errors)
          
            
            # Если есть ошибки - показываем их без расчёта
            if field_errors:
                error = "Пожалуйста, исправьте ошибки в форме"
            else:
                # Все проверки пройдены, выполняем расчёт
                try:
                    analysis = analyze_epidemic_scenario(
                        n=grid_size,
                        total_rats=total_rats,
                        weeks=weeks,
                        p_infect=p_infect,
                        p_move=p_move,
                        vacc_day=vacc_day,
                        vacc_percent=vacc_percent,
                    )
                    
                    results = {
                        'graph': analysis['graph'],
                        'threshold': analysis['results']['Эпидемический порог'],
                        'efficacy': float(analysis['evaluation']['Эффективность вакцинации'].rstrip('%')),
                        'peak_without': analysis['results']['Пик заражения (без вакцинации)'],
                        'peak_with': analysis['results']['Пик заражения (с вакцинацией)'],
                        'week_without': analysis['results']['Неделя пика (без вакцинации)'],
                        'week_with': analysis['results']['Неделя пика (с вакцинацией)'],
                        'matrix_display': analysis['simulation_result'].matrix_display,
                        'n': analysis['simulation_result'].n,
                        'epidemic_weeks_without': analysis['results']['Эпидемические недели (без вакцинации)'],
                        'epidemic_weeks_with': analysis['results']['Эпидемические недели (с вакцинацией)'],
                        'history_matrices': analysis['simulation_result'].history_matrices,
                        'total_days': analysis['simulation_result'].total_days
                    }
                except Exception as e:
                    error = f"Ошибка расчёта: {str(e)}"
                    import traceback
                    traceback.print_exc()
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

@route('/epidemic/export/csv', method='POST')
def export_epidemic_csv():
    """Экспорт данных симуляции в CSV"""
    try:
        # Получаем параметры из POST запроса и преобразуем в нужные имена
        params = {
            'n': int(request.forms.get('grid_size', 8)),
            'total_rats': int(request.forms.get('total_rats', 64)),
            'weeks': int(request.forms.get('weeks', 52)),
            'p_infect': float(request.forms.get('p_infect', 0.6)),
            'p_move': float(request.forms.get('p_move', 0.5)),
            'vacc_day': int(request.forms.get('vacc_day', 56)),
            'vacc_percent': int(request.forms.get('vacc_percent', 50))
        }
        
        # Запускаем симуляцию
        analysis = analyze_epidemic_scenario(**params)
        result = analysis['simulation_result']
        
        # Создаём CSV файл
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        
        # Заголовок
        writer.writerow(['Модель распространения эпидемии'])
        writer.writerow(['Параметры симуляции:'])
        writer.writerow(['Параметр', 'Значение'])
        writer.writerow(['Размер сетки', params['n']])
        writer.writerow(['Общее число крыс', params['total_rats']])
        writer.writerow(['Длительность (недели)', params['weeks']])
        writer.writerow(['Вероятность заражения', params['p_infect']])
        writer.writerow(['Вероятность перемещения', params['p_move']])
        writer.writerow(['День начала вакцинации', params['vacc_day']])
        writer.writerow(['Процент вакцинации', f"{params['vacc_percent']}%"])
        writer.writerow([])
        
        # Результаты
        writer.writerow(['Результаты симуляции:'])
        writer.writerow(['Показатель', 'Значение'])
        writer.writerow(['Эпидемический порог', result.threshold])
        writer.writerow(['Эффективность вакцинации', f"{result.efficacy}%"])
        writer.writerow(['Пик заражения (без вакцинации)', result.peak_without])
        writer.writerow(['Неделя пика (без вакцинации)', result.week_without])
        writer.writerow(['Пик заражения (с вакцинацией)', result.peak_with])
        writer.writerow(['Неделя пика (с вакцинацией)', result.week_with])
        writer.writerow(['Эпидемические недели (без вакцинации)', result.epidemic_weeks_without])
        writer.writerow(['Эпидемические недели (с вакцинацией)', result.epidemic_weeks_with])
        writer.writerow([])
        
        # Еженедельные данные
        writer.writerow(['Неделя', 'Здоровые (S)', 'Заражённые (I)', 'Иммунные (R)', 'Новые заражения'])
        for week in range(len(result.history_s)):
            new_infections = result.weekly_infections[week] if week < len(result.weekly_infections) else 0
            writer.writerow([
                week + 1,
                result.history_s[week],
                result.history_i[week],
                result.history_r[week],
                new_infections
            ])
        
        # Отправляем CSV файл
        response.content_type = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = 'attachment; filename="epidemic_data.csv"'
        
        # Добавляем BOM для корректного открытия в Excel
        csv_content = output.getvalue()
        return csv_content.encode('utf-8-sig')
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        response.status = 500
        return f"Ошибка экспорта: {str(e)}"


@route('/epidemic/export/graph', method='POST')
def export_epidemic_graph():
    """Экспорт графика в PNG"""
    try:
        import matplotlib.pyplot as plt
        from io import BytesIO
        
        # Получаем параметры из формы и преобразуем в нужные имена
        params = {
            'n': int(request.forms.get('grid_size', 8)),
            'total_rats': int(request.forms.get('total_rats', 64)),
            'weeks': int(request.forms.get('weeks', 52)),
            'p_infect': float(request.forms.get('p_infect', 0.6)),
            'p_move': float(request.forms.get('p_move', 0.5)),
            'vacc_day': int(request.forms.get('vacc_day', 56)),
            'vacc_percent': int(request.forms.get('vacc_percent', 50))
        }
        
        # Запускаем симуляцию
        analysis = analyze_epidemic_scenario(**params)
        result = analysis['simulation_result']
        
        # Создаём улучшенный график для экспорта
        plt.figure(figsize=(14, 8))
        
        weeks_range = list(range(len(result.history_s)))
        vacc_week = params['vacc_day'] / 7
        
        # График S, I, R
        plt.plot(weeks_range, result.history_s, 'g-', label='Здоровые (S)', linewidth=2)
        plt.plot(weeks_range, result.history_i, 'r-', label='Заражённые (I)', linewidth=2)
        plt.plot(weeks_range, result.history_r, 'orange', label='Иммунные (R)', linewidth=2)
        
        # Линия вакцинации
        if 0 <= vacc_week <= params['weeks']:
            plt.axvline(x=vacc_week, color='purple', linestyle='--', linewidth=2, 
                       label=f'Вакцинация (день {params["vacc_day"]})')
        
        # Отметка пика
        peak_week = result.week_with
        peak_value = result.peak_with
        plt.plot(peak_week, peak_value, 'ro', markersize=10, 
                label=f'Пик заражения: нед. {peak_week}, {peak_value} крыс')
        
        # Добавляем информацию о пороге на график
        if result.threshold > 0:
            plt.axhline(y=result.threshold, color='gray', linestyle=':', linewidth=1.5,
                       label=f'Эпидемический порог: {result.threshold}')
        
        # Настройка графика
        plt.xlabel('Недели', fontsize=12)
        plt.ylabel('Количество крыс', fontsize=12)
        plt.title(f'Динамика распространения эпидемии\nЭффективность вакцинации: {result.efficacy}%', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Сохраняем в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Отправляем PNG файл
        response.content_type = 'image/png'
        response.headers['Content-Disposition'] = 'attachment; filename="epidemic_graph.png"'
        
        return buf.getvalue()
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        response.status = 500
        return f"Ошибка экспорта: {str(e)}"


from controller.competition_controller import SimulationService, validate_parameters, prepare_display_data
from bottle import route, view, request, template, response, redirect
import time

# Глобальный сервис для симуляции
simulation_service = SimulationService()


@route('/competition', method=['GET', 'POST'])
def competition_page():
    """
    Главная страница симуляции конкуренции видов.
    Обрабатывает как GET (отображение), так и POST (действия) запросы.
    
    GET параметры:
        auto=1   - включить автоматический режим
        chart=1  - показать график динамики популяций
        speed=X  - скорость авто-режима в секундах (0.1-2.0)
    
    POST действия (action):
        randomize  - генерация случайных валидных параметров
        reset      - сброс симуляции с новыми параметрами
        auto_on    - включение автоматического режима
        auto_off   - выключение автоматического режима
        csv        - экспорт истории в CSV файл
        chart      - построение графика динамики популяций
    
    Returns:
        str: HTML страница с результатами симуляции
    """
    global simulation_service
    
    # Значения по умолчанию
    default_params = {
        'n': 4,
        'gray': 5,
        'white': 5,
        'rye': 8,
        'rye_interval': 3,
        'rye_spawn_count': 2,
        'max_ticks': 100
    }
    
    error = None
    csv_msg = None
    chart_path = None
    auto_mode = False
    speed = 0.5
    show_chart = False
    
    # Функция для генерации случайных валидных параметров
    def generate_random_params(self):
        """
        Генерирует случайные, но валидные параметры симуляции.
        
        Учитываются все ограничения:
        - Размер поля от 2 до 10
        - Крыс минимум 2 каждого вида
        - Сумма крыс не более total_cells - 1
        - Рожь не более total_cells - 4
        - Интервал и количество ржи в допустимых диапазонах
        
        Returns:
            dict: Словарь со случайными параметрами:
                - n: размер поля
                - gray: количество серых крыс
                - white: количество белых крыс
                - rye: количество ржи
                - rye_interval: интервал появления ржи
                - rye_spawn_count: количество новой ржи за раз
                - max_ticks: максимальное количество тактов
                - speed: скорость авто-режима
        """
        import random
    
        n = random.randint(2, 10)
        total_cells = n * n
    
        max_single_species = total_cells - 2
        max_total_rats = total_cells - 1
    
        if max_single_species < 2:
            max_single_species = 2
    
        gray = random.randint(2, min(max_single_species, 30))
    
        max_white = min(max_single_species, total_cells - 1 - gray)
        if max_white < 2:
            max_white = 2
            if gray + 2 > total_cells - 1:
                gray = max(2, total_cells - 1 - 2)
                max_white = 2
    
        white = random.randint(2, max_white)
    
        total_occupied = gray + white
        max_rye = min(total_cells - 4, total_cells - total_occupied)
        if max_rye < 1:
            max_rye = 1
        rye = random.randint(1, max_rye)
    
        rye_interval = random.randint(1, 20)
        rye_spawn_count = random.randint(1, 5)
        max_ticks = random.randint(1, 200)  
        speed = round(random.uniform(0.1, 2.0), 1)
    
        return {
            'n': n,
            'gray': gray,
            'white': white,
            'rye': rye,
            'rye_interval': rye_interval,
            'rye_spawn_count': rye_spawn_count,
            'max_ticks': max_ticks,
            'speed': speed
        }
    
    # Инициализируем параметры значениями по умолчанию
    n = default_params['n']
    gray_init = default_params['gray']
    white_init = default_params['white']
    rye_init = default_params['rye']
    rye_interval = default_params['rye_interval']
    rye_spawn_count = default_params['rye_spawn_count']
    max_ticks = default_params['max_ticks']
    
    # Функции для работы с сессией
    def get_session():
        """
        Восстанавливает данные сессии из HTTP-куки 'competition_session'.
        
        Формат хранения: pickle → base64 → строка ASCII.
        
        Returns:
            dict: Словарь с параметрами сессии или пустой словарь при ошибке
        """
        session_cookie = request.get_cookie('competition_session')
        if session_cookie:
            try:
                import pickle
                import base64
                return pickle.loads(base64.b64decode(session_cookie))
            except:
                return {}
        return {}

    def set_session(data):
        """
        Сохраняет данные сессии в HTTP-куку 'competition_session'.
        
        Формат хранения: pickle (сериализация) → base64 (ASCII) → кука.
        
        Args:
            data (dict): Словарь с параметрами для сохранения
        """
        import pickle
        import base64
        serialized = base64.b64encode(pickle.dumps(data)).decode()
        response.set_cookie('competition_session', serialized, path='/')
    
    session = get_session()
    
    # Получаем параметры из GET запроса
    if request.query.get('auto') == '1':
        auto_mode = True
    
    if request.query.get('chart') == '1':
        show_chart = True
    
    speed_param = request.query.get('speed', '')
    if speed_param:
        try:
            speed = float(speed_param.replace(',', '.'))
            if speed < 0.1:
                speed = 0.1
            elif speed > 2.0:
                speed = 2.0
        except:
            speed = 0.5
    
    # Обработка POST запросов
    if request.method == 'POST':
        action = request.forms.get('action', '')
        
        # Обработка генерации случайных значений
        if action == 'randomize':
            random_params = generate_random_params()
            n = random_params['n']
            gray_init = random_params['gray']
            white_init = random_params['white']
            rye_init = random_params['rye']
            rye_interval = random_params['rye_interval']
            rye_spawn_count = random_params['rye_spawn_count']
            max_ticks = random_params['max_ticks']
            speed = random_params['speed']
            
            session['n'] = n
            session['gray'] = gray_init
            session['white'] = white_init
            session['rye'] = rye_init
            session['rye_interval'] = rye_interval
            session['rye_spawn_count'] = rye_spawn_count
            session['max_ticks'] = max_ticks
            session['speed'] = speed
            set_session(session)
            
            simulation_service.reset()
            simulation_service.init_world(
                n, gray_init, white_init, rye_init,
                rye_interval, rye_spawn_count, max_ticks
            )
            auto_mode = False
            show_chart = False
            error = None
        
        # Обычная обработка параметров из формы
        else:
            n_str = request.forms.get('n', '').strip()
            if n_str:
                try:
                    n = int(n_str)
                except ValueError:
                    error = "Некорректное значение для размера поля"
            
            gray_str = request.forms.get('gray', '').strip()
            if gray_str:
                try:
                    gray_init = int(gray_str)
                except ValueError:
                    error = "Некорректное значение для количества серых крыс"
            
            white_str = request.forms.get('white', '').strip()
            if white_str:
                try:
                    white_init = int(white_str)
                except ValueError:
                    error = "Некорректное значение для количества белых крыс"
            
            rye_str = request.forms.get('rye', '').strip()
            if rye_str:
                try:
                    rye_init = int(rye_str)
                except ValueError:
                    error = "Некорректное значение для количества ржи"
            
            rye_interval_str = request.forms.get('rye_interval', '').strip()
            if rye_interval_str:
                try:
                    rye_interval = int(rye_interval_str)
                except ValueError:
                    error = "Некорректное значение для частоты ржи"
            
            rye_spawn_count_str = request.forms.get('rye_spawn_count', '').strip()
            if rye_spawn_count_str:
                try:
                    rye_spawn_count = int(rye_spawn_count_str)
                except ValueError:
                    error = "Некорректное значение для количества новой ржи"
            
            max_ticks_str = request.forms.get('max_ticks', '').strip()
            if max_ticks_str:
                try:
                    max_ticks = int(max_ticks_str)
                except ValueError:
                    error = "Некорректное значение для максимума тактов"
            
            speed_input = request.forms.get('speed', '')
            if speed_input:
                try:
                    speed = float(speed_input.replace(',', '.'))
                    if speed < 0.1:
                        speed = 0.1
                    elif speed > 2.0:
                        speed = 2.0
                except:
                    speed = 0.5
            
            # Сохраняем параметры в сессию (кроме action=reset)
            if action != 'reset':
                session['n'] = n
                session['gray'] = gray_init
                session['white'] = white_init
                session['rye'] = rye_init
                session['rye_interval'] = rye_interval
                session['rye_spawn_count'] = rye_spawn_count
                session['max_ticks'] = max_ticks
                session['speed'] = speed
                set_session(session)
            
            # Валидация параметров
            if not error:
                total_cells = n * n
                
                if not (2 <= n <= 10):
                    error = "Размер поля n должен быть в диапазоне от 2 до 10"
                elif gray_init < 2:
                    error = f"Количество серых крыс должно быть не менее 2 (было {gray_init})"
                elif gray_init > total_cells - 2:
                    error = f"Количество серых крыс не может превышать {total_cells - 2}"
                elif white_init < 2:
                    error = f"Количество белых крыс должно быть не менее 2 (было {white_init})"
                elif white_init > total_cells - 2:
                    error = f"Количество белых крыс не может превышать {total_cells - 2}"
                elif gray_init + white_init > total_cells - 1:
                    error = f"Сумма крыс ({gray_init + white_init}) не должна превышать {total_cells - 1}"
                elif rye_init < 1:
                    error = f"Количество ржи должно быть не менее 1 (было {rye_init})"
                elif rye_init > total_cells - 4:
                    error = f"Количество ржи не может превышать {total_cells - 4}"
                elif not (1 <= rye_interval <= 20):
                    error = "Частота появления ржи должна быть в диапазоне от 1 до 20"
                elif not (1 <= rye_spawn_count <= 5):
                    error = "Количество новой ржи за раз должно быть в диапазоне от 1 до 5"
                elif not (1 <= max_ticks <= 200):
                    error = "Максимум тактов должен быть в диапазоне от 1 до 200"
            
            # Обработка действий
            if action == 'reset' and not error:
                simulation_service.reset()
                simulation_service.init_world(
                    n, gray_init, white_init, rye_init,
                    rye_interval, rye_spawn_count, max_ticks
                )
                auto_mode = False
                show_chart = False
                session['n'] = n
                session['gray'] = gray_init
                session['white'] = white_init
                session['rye'] = rye_init
                session['rye_interval'] = rye_interval
                session['rye_spawn_count'] = rye_spawn_count
                session['max_ticks'] = max_ticks
                session['speed'] = speed
                set_session(session)

            elif action == 'auto_on' and not error:
                auto_mode = True
                show_chart = False
                if not simulation_service.world:
                    simulation_service.init_world(
                        n, gray_init, white_init, rye_init,
                        rye_interval, rye_spawn_count, max_ticks
                    )
                if simulation_service.world and not simulation_service.world.is_simulation_over():
                    simulation_service.run_tick()
            
            elif action == 'auto_off':
                auto_mode = False
                show_chart = False
            
            elif action == 'csv' and not error:
                if simulation_service.world:
                    filename = simulation_service.export_csv()
                    if filename:
                        csv_msg = f"CSV файл сохранён: {filename}"
                    else:
                        error = "Нет данных для экспорта"
                else:
                    error = "Нет данных для экспорта"
                show_chart = False
            
            elif action == 'chart' and not error:
                if simulation_service.world:
                    chart_path = simulation_service.get_chart()
                    if chart_path:
                        show_chart = True
                    else:
                        error = "Недостаточно данных для построения графика (нужно хотя бы 2 такта)"
                else:
                    error = "Нет данных для построения графика"
    else:
        # GET запрос - загружаем параметры из сессии, если они есть
        if 'n' in session:
            n = session.get('n', default_params['n'])
            gray_init = session.get('gray', default_params['gray'])
            white_init = session.get('white', default_params['white'])
            rye_init = session.get('rye', default_params['rye'])
            rye_interval = session.get('rye_interval', default_params['rye_interval'])
            rye_spawn_count = session.get('rye_spawn_count', default_params['rye_spawn_count'])
            max_ticks = session.get('max_ticks', default_params['max_ticks'])
            speed = session.get('speed', 0.5)
    
    # Если авторежим включён и это GET запрос, делаем шаг
    if auto_mode and request.method == 'GET' and not error:
        if simulation_service.world:
            if not simulation_service.world.is_simulation_over() and simulation_service.world.tick < max_ticks:
                simulation_service.run_tick()
    
    # Если мир не инициализирован, создаём с текущими параметрами
    if not simulation_service.world:
        simulation_service.init_world(
            n, gray_init, white_init, rye_init,
            rye_interval, rye_spawn_count, max_ticks
        )
    
    # ДОБАВЛЯЕМ РОЖЬ ЕСЛИ ЕЁ НЕТ (для стимуляции размножения)
    if simulation_service.world and simulation_service.world.rye_count == 0 and simulation_service.world.tick > 0:
        import random
        empty_cells = [(i, j) for i in range(simulation_service.world.n) 
                      for j in range(simulation_service.world.n)
                      if not simulation_service.world.grid[i][j].rats 
                      and not simulation_service.world.grid[i][j].rye]
        for _ in range(min(3, len(empty_cells))):
            if empty_cells:
                x, y = random.choice(empty_cells)
                simulation_service.world.grid[x][y].rye = True
                simulation_service.world.rye_count += 1
                empty_cells.remove((x, y))
        print(f"DEBUG: Added emergency rye, now rye_count={simulation_service.world.rye_count}")
    
    # Получаем состояние мира
    world_state = simulation_service.get_world_state()
    extinct = world_state.get('is_extinct', False) if world_state else False

    if extinct and auto_mode:
        auto_mode = False

    cell_class, cell_content = prepare_display_data(world_state)

    if world_state:
        tick = world_state.get('tick', 0)
        gray_count = world_state.get('gray', 0)
        white_count = world_state.get('white', 0)
        rye_count = world_state.get('rye', 0)
        fights = world_state.get('fights', 0)
        deaths = world_state.get('deaths', 0)
    else:
        tick = 0
        gray_count = gray_init
        white_count = white_init
        rye_count = rye_init
        fights = 0
        deaths = 0
    
    K = (n * n) // 2
    
    if gray_count > 0 and white_count > 0:
        alpha = round(white_count / K if K > 0 else 1, 3)
        beta = round(gray_count / K if K > 0 else 1, 3)
    else:
        alpha = 0
        beta = 0
    
    if alpha * beta != 1 and K > 0:
        denominator = 1 - alpha * beta
        if denominator != 0:
            g_star = round(K * (1 - alpha) / denominator, 2)
            w_star = round(K * (1 - beta) / denominator, 2)
        else:
            g_star = 0
            w_star = 0
    else:
        g_star = 0
        w_star = 0
    
    if show_chart and not chart_path and simulation_service.world:
        chart_path = simulation_service.get_chart()
    
    template_data = {
        'year': datetime.now().year,
        'n': n,
        'gray': gray_init,
        'white': white_init,
        'rye': rye_init,
        'rye_interval': rye_interval,
        'rye_spawn_count': rye_spawn_count,
        'max_ticks': max_ticks,
        'auto': auto_mode,
        'speed': speed,
        'error': error,
        'csv_msg': csv_msg,
        'chart': chart_path if show_chart else None,
        'show_chart': show_chart,
        'extinct': extinct,
        'tick': tick,
        'gray_count': gray_count,
        'white_count': white_count,
        'rye_count': rye_count,
        'fights': fights,
        'deaths': deaths,
        'verdict': simulation_service.get_verdict() if simulation_service.world else "Нет данных",
        'cell_class': cell_class,
        'cell_content': cell_content,
        'K': K,
        'alpha': alpha,
        'beta': beta,
        'g_star': g_star,
        'w_star': w_star
    }
    
    return template('competition', **template_data)

@route('/competition/export/csv', method=['POST'])
def export_competition_csv():
    """Экспорт данных симуляции в CSV"""
    global simulation_service
    
    if simulation_service.world:
        filename = simulation_service.export_csv()
        if filename:
            # Отправляем файл пользователю
            from bottle import static_file
            import os
            return static_file(os.path.basename(filename), root='logs', download=True)
        else:
            return "Нет данных для экспорта"
    else:
        return "Симуляция не инициализирована"


@route('/competition/export/chart', method=['POST'])
def export_competition_chart():
    """Экспорт графика в PNG"""
    chart_path = request.forms.get('chart_path', '')
    
    if chart_path and chart_path.startswith('/static/charts/'):
        import os
        filename = os.path.basename(chart_path)
        from bottle import static_file
        return static_file(filename, root='static/charts', download=f"competition_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    else:
        # Если нет сохранённого графика, генерируем новый
        global simulation_service
        if simulation_service.world:
            chart_path = simulation_service.get_chart()
            if chart_path:
                import os
                filename = os.path.basename(chart_path)
                from bottle import static_file
                return static_file(filename, root='static/charts', download=f"competition_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        return "Нет графика для экспорта"



    # Подготовка данных для отображения поля
    cell_class, cell_content = prepare_display_data(world_state)
    
    # Отладка - проверка размеров
    if len(cell_class) != n:
        print(f"Warning: cell_class size ({len(cell_class)}) != n ({n})")
        # Дополняем до нужного размера
        while len(cell_class) < n:
            cell_class.append(['cell-empty'] * n)
            cell_content.append(['⬜'] * n)
    
    for i in range(len(cell_class)):
        if len(cell_class[i]) != n:
            print(f"Warning: cell_class[{i}] size ({len(cell_class[i])}) != n ({n})")
            while len(cell_class[i]) < n:
                cell_class[i].append('cell-empty')
                cell_content[i].append('⬜')




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