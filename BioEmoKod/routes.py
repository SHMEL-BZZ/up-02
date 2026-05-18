"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt
import random

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
    
    if request.method == 'POST':
        try:
            # Получаем параметры из формы
            x0 = float(request.forms.get('x0', 50))
            y0 = float(request.forms.get('y0', 20))
            alpha = float(request.forms.get('alpha', 0.8))
            c = float(request.forms.get('c', 0.04))
            beta = float(request.forms.get('beta', 0.6))
            d = float(request.forms.get('d', 0.02))
            T = float(request.forms.get('T', 50))
            N = int(request.forms.get('N', 1000))
            
            # Валидация параметров
            if not (10 <= x0 <= 100):
                raise ValueError("Численность жертв должна быть в диапазоне 10–100")
            if not (1 <= y0 <= 50):
                raise ValueError("Численность хищников должна быть в диапазоне 1–50")
            if not (0.4 <= alpha <= 1.5):
                raise ValueError("α должно быть в диапазоне 0.4–1.5")
            if not (0.01 <= c <= 0.06):
                raise ValueError("c должно быть в диапазоне 0.01–0.06")
            if not (0.4 <= beta <= 1.5):
                raise ValueError("β должно быть в диапазоне 0.4–1.5")
            if not (0.01 <= d <= 0.06):
                raise ValueError("d должно быть в диапазоне 0.01–0.06")
            if not (5 <= T <= 50):
                raise ValueError("Длительность T должна быть в диапазоне 5–50")
            if not (200 <= N <= 10000):
                raise ValueError("Число шагов N должно быть в диапазоне 200–10000")
           
            # Запускаем симуляцию
            result = simulate_lotka_volterra(
                x0=x0, y0=y0, alpha=alpha, c=c, beta=beta, d=d, T=T, N=N
            )
            
            # Генерируем график
            plot_base64 = plot_dynamics(result)
            
            # Формируем результаты из реальных данных
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
            
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Ошибка расчёта: {str(e)}"
    
    # Для GET запроса или после обработки POST
    return template('predator_pray', 
                   title=title, 
                   year=datetime.now().year,
                   results=results,
                   error=error)


from model.epidemic import EpidemicSimulation

from model.epidemic import EpidemicSimulation

@route('/epidemic', method=['GET', 'POST'])
def epidemic():
    """Renders the epidemic page and handles form submission."""
    title = 'Модель «Распространение эпидемии»'
    results = None
    error = None
    
    if request.method == 'POST':
        try:
            # Получаем параметры из формы
            params = {
                'grid_size': int(request.forms.get('grid_size', 8)),
                'total_rats': int(request.forms.get('total_rats', 64)),
                'weeks': int(request.forms.get('weeks', 52)),
                'p_infect': float(request.forms.get('p_infect', 0.6)),
                'p_move': float(request.forms.get('p_move', 0.5)),
                'vacc_day': int(request.forms.get('vacc_day', 56)),
                'vacc_percent': int(request.forms.get('vacc_percent', 50))
            }
            
            # Валидация параметров
            if not (2 <= params['grid_size'] <= 10):
                raise ValueError("Размер сетки n должен быть в диапазоне 2–10")
            max_rats = params['grid_size'] * params['grid_size'] * 4
            if not (1 <= params['total_rats'] <= max_rats):
                raise ValueError(f"Число крыс должно быть в диапазоне 1–{max_rats}")
            if not (8 <= params['weeks'] <= 260):
                raise ValueError("Длительность симуляции должна быть в диапазоне 8–260 недель")
            if not (0.1 <= params['p_infect'] <= 0.9):
                raise ValueError("Вероятность заражения должна быть в диапазоне 0.1–0.9")
            if not (0.1 <= params['p_move'] <= 0.9):
                raise ValueError("Вероятность перемещения должна быть в диапазоне 0.1–0.9")
            max_vacc_day = params['weeks'] * 7
            if not (9 <= params['vacc_day'] <= max_vacc_day):
                raise ValueError(f"День вакцинации должен быть в диапазоне 9–{max_vacc_day}")
            if not (1 <= params['vacc_percent'] <= 100):
                raise ValueError("Процент вакцинации должен быть в диапазоне 1–100")
            
            # Запускаем симуляцию
            sim = EpidemicSimulation(params)
            sim_results = sim.get_results()
            
            # Вычисляем снижение пика
            peak_without = sim_results['peak_without']
            peak_with = sim_results['peak_with']
            if peak_without > 0:
                reduction = round((peak_without - peak_with) / peak_without * 100, 1)
            else:
                reduction = 0
            
            # Формируем результаты для шаблона
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
            
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Ошибка расчёта: {str(e)}"
    
    # Для GET запроса или после обработки POST
    return template('epidemic', 
                   title=title, 
                   year=datetime.now().year,
                   results=results,
                   error=error)


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
    
    if request.method == 'POST':
        try:
            # Получаем параметры из формы
            N = int(request.forms.get('N', 15))
            M = int(request.forms.get('M', 15))
            K = int(request.forms.get('K', 50))
            p_repro = float(request.forms.get('p_repro', 0.25))
            p_death = float(request.forms.get('p_death', 0.1))
            
            
            
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
           
            
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Ошибка расчёта: {str(e)}"
    
    # Для GET или после POST с ошибкой отдаём форму
    return template('fishing',
                   title=title,
                   year=datetime.now().year,
                   results=results,
                   error=error)

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        year=datetime.now().year
    )