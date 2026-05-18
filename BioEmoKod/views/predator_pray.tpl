% rebase('layout.tpl', title=title, year=year, active_page='predator_pray')

<!-- специальный стиль для страницы Модель хищник-жертва -->
<head>
    <link rel="stylesheet" type="text/css" href="/static/content/predator_pray.css" />
</head>

<div class="page-header">
    <h2>Модель «Хищник-жертва»</h2>
</div>

<!-- БЛОК-ЯКОРЬ ДЛЯ БЫСТРОГО ПЕРЕХОДА К РАСЧЁТНОЙ ПАНЕЛИ -->
<div class="calculation-jump">
    <div class="calculation-jump__content">
        <span class="calculation-jump__text">⚡ Хотите провести расчёт?</span>
        <a href="#calculation-panel" class="calculation-jump__btn">
            🚀 Перейти к расчётной панели
        </a>
    </div>
</div>

<!-- Верхняя строка: теория + картинки в колонке -->
<div class="row">
    <div class="col-md-8">
        <!-- БЛОК ТЕОРИИ (аккордеон) -->
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📖 Теоретические сведения</h3>
            </div>
            <div class="panel-body">
                <div class="panel-group" id="accordion">
                    <!-- 1. Модель Лотки–Вольтерры -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
                                    🦊 Модель «Хищник-жертва» (Лотки-Вольтерры)
                                </a>
                            </h4>
                        </div>
                        <div id="collapse1" class="panel-collapse collapse in">
                            <div class="panel-body">
                                <p>Модель описывает взаимодействие двух популяций:</p>
                                <ul>
                                    <li><strong>x(t)</strong> — численность жертв (кроликов) в момент времени t</li>
                                    <li><strong>y(t)</strong> — численность хищников (лис) в момент времени t</li>
                                </ul>
                                <p><strong>Основные предположения:</strong></p>
                                <ul>
                                    <li>Жертвы размножаются пропорционально своей численности</li>
                                    <li>Жертвы погибают при встречах с хищниками</li>
                                    <li>Хищники размножаются за счёт съеденных жертв</li>
                                    <li>Хищники гибнут от голода пропорционально своей численности</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- 2. Система уравнений -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">
                                    📐 Система дифференциальных уравнений
                                </a>
                            </h4>
                        </div>
                        <div id="collapse2" class="panel-collapse collapse">
                            <div class="panel-body">
                                <p>Динамика системы описывается двумя уравнениями:</p>
                                <div class="well well-sm text-center">
                                    <p><strong>dx/dt = α·x − c·x·y</strong></p>
                                    <p><strong>dy/dt = d·x·y − β·y</strong></p>
                                </div>
                                <p><strong>Параметры модели:</strong></p>
                                <ul>
                                    <li><strong>α</strong> — скорость размножения жертв (кроликов)</li>
                                    <li><strong>c</strong> — эффективность охоты хищников (встречаемость)</li>
                                    <li><strong>β</strong> — скорость гибели хищников от голода</li>
                                    <li><strong>d</strong> — вклад съеденной жертвы в размножение хищников</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Равновесие и устойчивость -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">
                                    ⚖️ Равновесие и анализ устойчивости
                                </a>
                            </h4>
                        </div>
                        <div id="collapse3" class="panel-collapse collapse">
                            <div class="panel-body">
                                <p><strong>Ненулевое равновесие</strong> (когда оба вида существуют):</p>
                                <div class="well well-sm text-center">
                                    <p><strong>x* = β/d</strong> — равновесная численность жертв</p>
                                    <p><strong>y* = α/c</strong> — равновесная численность хищников</p>
                                </div>
                                <p><strong>Тип устойчивости:</strong> «центр» — колебательный режим.</p>
                                <p><strong>Период малых колебаний:</strong></p>
                                <div class="well well-sm text-center">
                                    <p><strong>T = 2π / √(α·β)</strong></p>
                                </div>
                                <p><em>При больших амплитудах период может быть больше на 10–20%.</em></p>
                            </div>
                        </div>
                    </div>

                    <!-- 4. Примеры сценариев -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse4">
                                    📊 Примеры сценариев
                                </a>
                            </h4>
                        </div>
                        <div id="collapse4" class="panel-collapse collapse">
                            <div class="panel-body">
                                <p><strong>Пример 1. Классические колебания:</strong></p>
                                <ul>
                                    <li>α = 0.8, c = 0.04, β = 0.6, d = 0.02</li>
                                    <li>x₀ = 50, y₀ = 20</li>
                                    <li>Результат: циклические колебания численности</li>
                                </ul>
                                <p><strong>Пример 2. Вымирание хищников:</strong></p>
                                <ul>
                                    <li>α = 0.5, c = 0.01, β = 1.2, d = 0.01</li>
                                    <li>x₀ = 30, y₀ = 5</li>
                                    <li>Результат: хищники вымирают из-за высокой смертности</li>
                                </ul>
                                <p><strong>Пример 3. Вымирание жертв:</strong></p>
                                <ul>
                                    <li>α = 0.4, c = 0.08, β = 0.5, d = 0.01</li>
                                    <li>x₀ = 10, y₀ = 30</li>
                                    <li>Результат: жертвы истребляются хищниками</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- 5. Источники -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse5">
                                    📚 Источники
                                </a>
                            </h4>
                        </div>
                        <div id="collapse5" class="panel-collapse collapse">
                            <div class="panel-body">
                                <ul>
                                    <li>Лотка А. Дж. — «Элементы физической биологии» (1925)</li>
                                    <li>Вольтерра В. — «Математическая теория борьбы за существование» (1931)</li>
                                    <li><a href="https://math-it.petrsu.ru/users/semenova/MathECO/Lections/Lotka_Volterra.pdf" target="_blank">Математическая модель Лотки-Вольтерры (PDF)</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div> 
            </div> 
        </div> 
    </div>

    <!-- Картинки в колонке справа -->
    <div class="col-md-4">
        <div class="panel panel-default">
            <div class="panel-body text-center">
                <div class="row">
                    <div class="col-xs-12">
                        <img src="/static/img/bunny.jpg"
                             class="img-responsive predator-prey-img"
                             alt="Заяц">
                        <p class="text-muted">🐇 Жертва (заяц)</p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-12">
                        <img src="/static/img/fox.jpg"
                             class="img-responsive predator-prey-img"
                             alt="Лиса">
                        <p class="text-muted">🦊 Хищник (лиса)</p>
                    </div>
                </div>
            </div> 
        </div> 
    </div> 
</div> 

<!-- Расчётная панель -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-primary" id="calculation-panel">
            <div class="panel-heading">
                <h3 class="panel-title text-center">Расчётная панель</h3>
            </div>
            <div class="panel-body">
                <form action="/predator_pray" method="post" class="form-horizontal" id="calculationForm" novalidate>
                    <div class="row">
                        <!-- ЛЕВАЯ КОЛОНКА -->
                        <div class="col-md-6">
                            <h4 class="text-center">📌 Начальные условия</h4>
                            <div class="form-group" id="group-x0">
                                <label class="col-sm-6 control-label">Число жертв x₀:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="any" name="x0" id="x0" class="form-control" value="50" required>
                                    <span class="help-block">Диапазон: 10–100</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-y0">
                                <label class="col-sm-6 control-label">Число хищников y₀:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="any" name="y0" id="y0" class="form-control" value="20" required>
                                    <span class="help-block">Диапазон: 1–50</span>
                                </div>
                            </div>

                            <hr>

                            <h4 class="text-center">⏱️ Параметры симуляции</h4>
                            <div class="form-group" id="group-T">
                                <label class="col-sm-6 control-label">Длительность T (лет):</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="1" name="T" id="T" class="form-control" value="50" required>
                                    <span class="help-block">Диапазон: 5–50</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-N">
                                <label class="col-sm-6 control-label">Число шагов N:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="100" name="N" id="N" class="form-control" value="1000" required>
                                    <span class="help-block">Диапазон: 200–10000</span>
                                </div>
                            </div>
                        </div>

                        <!-- ПРАВАЯ КОЛОНКА -->
                        <div class="col-md-6">
                            <h4 class="text-center">⚙️ Параметры модели</h4>
                            <div class="form-group" id="group-alpha">
                                <label class="col-sm-6 control-label">Рождаемость жертв α:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="0.01" name="alpha" id="alpha" class="form-control" value="0.8" required>
                                    <span class="help-block">Диапазон: 0.4–1.5</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-c">
                                <label class="col-sm-6 control-label">Эффективность охоты c:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="0.01" name="c" id="c" class="form-control" value="0.04" required>
                                    <span class="help-block">Диапазон: 0.01–0.06</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-beta">
                                <label class="col-sm-6 control-label">Смертность хищников β:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="0.01" name="beta" id="beta" class="form-control" value="0.6" required>
                                    <span class="help-block">Диапазон: 0.4–1.5</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-d">
                                <label class="col-sm-6 control-label">Рост хищников d:</label>
                                <div class="col-sm-6" style="position: relative;">
                                    <input type="number" step="0.01" name="d" id="d" class="form-control" value="0.02" required>
                                    <span class="help-block">Диапазон: 0.01–0.06</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr>

                    <div class="form-group">
                        <div class="col-sm-offset-4 col-sm-4">
                            <button type="submit" class="btn btn-success btn-block" id="submitBtn">▶ Запустить расчёт</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- JavaScript для валидации -->
<script>
// Правила валидации
const validationRules = {
    x0: { min: 10, max: 100, message: 'Число жертв должно быть в диапазоне 10–100' },
    y0: { min: 1, max: 50, message: 'Число хищников должно быть в диапазоне 1–50' },
    T: { min: 5, max: 50, message: 'Длительность должна быть в диапазоне 5–50 лет' },
    N: { min: 200, max: 10000, message: 'Число шагов должно быть в диапазоне 200–10000' },
    alpha: { min: 0.4, max: 1.5, message: 'Рождаемость жертв должна быть в диапазоне 0.4–1.5' },
    c: { min: 0.01, max: 0.06, message: 'Эффективность охоты должна быть в диапазоне 0.01–0.06' },
    beta: { min: 0.4, max: 1.5, message: 'Смертность хищников должна быть в диапазоне 0.4–1.5' },
    d: { min: 0.01, max: 0.06, message: 'Рост хищников должен быть в диапазоне 0.01–0.06' }
};

// Функция проверки одного поля
function validateField(fieldId) {
    const field = document.getElementById(fieldId);
    const value = parseFloat(field.value);
    const rule = validationRules[fieldId];
    const formGroup = document.getElementById(`group-${fieldId}`);
    const inputWrapper = field.parentElement;
    
    // Удаляем старые иконки
    const oldIcon = inputWrapper.querySelector('.error-icon');
    const oldTooltip = inputWrapper.querySelector('.error-tooltip');
    if (oldIcon) oldIcon.remove();
    if (oldTooltip) oldTooltip.remove();
    
    // Проверка
    if (isNaN(value) || value < rule.min || value > rule.max) {
        formGroup.classList.add('has-error');
        formGroup.classList.remove('has-success');
        
        // Иконка
        const errorIcon = document.createElement('div');
        errorIcon.className = 'error-icon';
        errorIcon.innerHTML = '<span>⚠️</span>';
        
        // Подсказка
        const tooltip = document.createElement('div');
        tooltip.className = 'error-tooltip';
        tooltip.innerHTML = `⚠️ ${rule.message}`;
        
        inputWrapper.appendChild(errorIcon);
        inputWrapper.appendChild(tooltip);
        return false;
    } else {
        formGroup.classList.remove('has-error');
        formGroup.classList.add('has-success');
        return true;
    }
}

// Проверка всех полей
function validateAllFields() {
    let isValid = true;
    for (const fieldId in validationRules) {
        if (!validateField(fieldId)) isValid = false;
    }
    return isValid;
}

// Показать сообщение об ошибке
function showErrorSummary() {
    const existing = document.querySelector('.validation-summary');
    if (existing) existing.remove();
    
    const summary = document.createElement('div');
    summary.className = 'alert alert-danger validation-summary';
    summary.innerHTML = `
        <strong>⚠️ Ошибка валидации!</strong><br>
        Исправьте поля с красной рамкой
        <button type="button" class="close" onclick="this.parentElement.remove()">&times;</button>
    `;
    document.body.appendChild(summary);
    setTimeout(() => summary.remove(), 5000);
}

// Подписка на события
document.addEventListener('DOMContentLoaded', function() {
    for (const fieldId in validationRules) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', () => validateField(fieldId));
            field.addEventListener('blur', () => validateField(fieldId));
        }
    }
    
    const form = document.getElementById('calculationForm');
    form.addEventListener('submit', function(e) {
        if (!validateAllFields()) {
            e.preventDefault();
            showErrorSummary();
            const firstError = document.querySelector('.has-error');
            if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
    
    // Первоначальная проверка
    validateAllFields();
});
</script>

<!-- Отображение ошибок сервера -->
% if defined('error') and error:
<div class="row">
    <div class="col-md-12">
        <div class="alert alert-danger">
            <strong>⚠️ Ошибка:</strong> {{ error }}
            <button type="button" class="close" data-dismiss="alert">×</button>
        </div>
    </div>
</div>
% end

<!-- Результаты расчёта -->
% if defined('results') and results:
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-success">
            <div class="panel-heading">
                <h3 class="panel-title text-center">Результаты моделирования</h3>
            </div>
            <div class="panel-body">
                <div class="row">
                    <div class="col-md-12">
                        <h4 class="text-center">Динамика популяций и фазовый портрет</h4>
                        <img src="data:image/png;base64,{{ results.get('plot_base64', '') }}" 
                             class="img-responsive img-thumbnail results-plot"
                             alt="Графики динамики и фазовый портрет">
                    </div>
                </div>

                <hr>

                <div class="row">
                    <div class="col-md-12">
                        <div class="panel-heading">
                            <h4 class="text-center">Анализ результатов</h4>
                        </div>
                        <div class="well">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Равновесная численность жертв (x*):</strong> {{ results.get('x_star', 'Н/Д') }}</p>
                                    <p><strong>Равновесная численность хищников (y*):</strong> {{ results.get('y_star', 'Н/Д') }}</p>
                                    <p><strong>Расчётный период колебаний:</strong> {{ results.get('period', 'Н/Д') }} лет</p>
                                    <p><strong>Тип устойчивости:</strong> {{ results.get('stability_type', 'Н/Д') }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Средняя численность жертв:</strong> {{ results.get('avg_prey', 'Н/Д') }}</p>
                                    <p><strong>Средняя численность хищников:</strong> {{ results.get('avg_predator', 'Н/Д') }}</p>
                                    <p><strong>Мин/макс жертв:</strong> {{ results.get('min_prey', 'Н/Д') }} / {{ results.get('max_prey', 'Н/Д') }}</p>
                                    <p><strong>Мин/макс хищников:</strong> {{ results.get('min_predator', 'Н/Д') }} / {{ results.get('max_predator', 'Н/Д') }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Кнопка экспорта -->
                <div class="text-center">
                    <form action="/export_csv" method="post" style="display: inline;">
                        <input type="hidden" name="data_type" value="predator_prey">
                        <button type="submit" class="btn btn-primary">Экспорт данных в CSV</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
% end