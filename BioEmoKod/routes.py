"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Для работы без графического интерфейса
import matplotlib.pyplot as plt

# Импортируем вашу модель 
from model.pp_model import simulate_lotka_volterra, plot_dynamics

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
                'plot_base64': plot_base64  # Раскомментировали!
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


@route('/epidemic')
@view('epidemic')
def epidemic():
    """Renders the epidemic page."""
    return dict(
        title='Epidemic',
        year=datetime.now().year
    )


@route('/competition')
@view('competition')
def competition():
    """Renders the competition page."""
    return dict(
        title='Competition',
        year=datetime.now().year
    )


@route('/fishing')
@view('fishing')
def fishing():
    """Renders the fishing page."""
    return dict(
        title='Fishing',
        year=datetime.now().year
    )


@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        year=datetime.now().year
    )