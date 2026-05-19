"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, response
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt
import random
import csv
import io

# Импортируем вашу модель 
from model.pp_model import simulate_lotka_volterra, plot_dynamics
from controller.fishing_controller import find_optimal_q

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


from model.epidemic import SimulationResult
from controller.epidemic_controller import plot_epidemic_dynamics, plot_comparison_chart, analyze_epidemic_scenario

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
                    'epidemic_weeks_with': analysis['results']['Эпидемические недели (с вакцинацией)']
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
                        'epidemic_weeks_with': analysis['results']['Эпидемические недели (с вакцинацией)']
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