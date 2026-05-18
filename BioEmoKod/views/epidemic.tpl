% rebase('layout.tpl', title=title, year=year, active_page='epidemic')

<!-- Подключение уникальных стилей для страницы эпидемии -->
<link rel="stylesheet" type="text/css" href="/static/content/epidemic.css" />

<div class="page-header">
    <h2>Модель «Распространение эпидемии»</h2>
</div>

<!-- Кнопка перехода к расчётной панели -->
<div class="jump-button">
    <a href="#calculate" class="btn btn-jump">⬇ Перейти к расчётам</a>
</div>

<!-- теоретический блок (оставляем без изменений) -->
<div class="row">
    <div class="col-md-7">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📖 Теоретические сведения</h3>
            </div>
            <div class="panel-body">
                <div class="panel-group" id="accordion">
                    <!-- 1. Описание модели -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
                                    🐭 Модель распространения инфекции (SIR на сетке)
                                </a>
                            </h4>
                        </div>
                        <div id="collapse1" class="panel-collapse collapse in">
                            <div class="panel-body">
                                <p>Модель описывает распространение инфекции в популяции крыс, обитающих на двумерной сетке n×n. Каждая клетка может содержать до 4 особей.</p>
                                <p>Состояния особей:</p>
                                <ul>
                                    <li><strong style="color: #2ecc71;">S (Susceptible)</strong> — здоровые, восприимчивые к заражению</li>
                                    <li><strong style="color: #e74c3c;">I (Infectious)</strong> — заражённые (инфекционные), болеют 6 дней</li>
                                    <li><strong style="color: #f1c40f;">R (Recovered)</strong> — невосприимчивые (иммунитет на 4 дня)</li>
                                </ul>
                                <p>Ключевые механизмы: перемещение в соседние клетки, заражение при контакте, циклический переход S→I→R→S, вакцинация.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 2. Параметры и алгоритм -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">
                                    ⚙️ Параметры и алгоритм
                                </a>
                            </h4>
                        </div>
                        <div id="collapse2" class="panel-collapse collapse">
                            <div class="panel-body">
                                <p>Входные параметры модели:</p>
                                <ul>
                                    <li>n — размер сетки (n×n клеток)</li>
                                    <li>rats — общее количество особей</li>
                                    <li>p_infect — вероятность заражения при контакте</li>
                                    <li>p_move — вероятность перемещения в соседнюю клетку</li>
                                    <li>t — длительность симуляции (в неделях)</li>
                                    <li>day_vac — день начала вакцинации</li>
                                    <li>v — доля вакцинируемых здоровых особей</li>
                                </ul>
                                <p><strong>Алгоритм одного дня:</strong> перемещение → заражение → прогресс болезни/иммунитета → вакцинация.</p>
                                <p><strong>Фиксированные параметры:</strong> болезнь = 6 дней, иммунитет = 4 дня.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Формулы расчёта -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">
                                    📐 Формулы расчёта показателей
                                </a>
                            </h4>
                        </div>
                        <div id="collapse3" class="panel-collapse collapse">
                            <div class="panel-body">
                                <div class="formula-compact">
                                    <h5>📊 Эпидемический порог</h5>
                                    <div class="formula-box formula-box-green">
                                        <p class="formula-text">X̄ = (X₁+...+X₈)/8</p>
                                        <p class="formula-text">σ = √[Σ(Xᵢ-X̄)²/7]</p>
                                        <p class="formula-text">X<sub>порог</sub> = X̄ + 2,507·σ</p>
                                    </div>
                                    <p class="formula-note">* на основе первых 8 недель (коэф. Стьюдента)</p>
                                </div>

                                <div class="formula-compact">
                                    <h5>💉 Эффективность вакцинации</h5>
                                    <div class="formula-box formula-box-green">
                                        <p class="formula-text">Эфф = (W<sub>без</sub> - W<sub>с</sub>) / W<sub>без</sub> × 100%</p>
                                    </div>
                                    <p class="formula-note">W — количество эпидемических недель</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Справа: краткие определения -->
    <div class="col-md-5">
        <div class="definitions">
            <div class="def-card">
                <div class="def-title">Эпидемический порог</div>
                <p>Эпидемический порог — это математически рассчитанный уровень заболеваемости инфекцией, при превышении которого начинается её массовое (эпидемическое) распространение среди населения на конкретной территории.</p>
            </div>
            <div class="def-card">
                <div class="def-title">Эффективность вакцинации</div>
                <p>Эффективность вакцинации — это степень защиты привитого населения от конкретной инфекции, измеряемая в клинических (испытания) или реальных условиях. Она оценивается по показателю снижения заболеваемости среди вакцинированных по сравнению с невакцинированными.</p>
            </div>
            <div class="def-card">
                <div class="def-title">Анализ результатов вакцинации</div>
                <div class="analysis-badges">
                    <div class="analysis-badge badge-low">
                        <strong>Низкая</strong>
                        <span>&lt; 50%</span>
                    </div>
                    <div class="analysis-badge badge-medium">
                        <strong>Средняя</strong>
                        <span>50% – 80%</span>
                    </div>
                    <div class="analysis-badge badge-high">
                        <strong>Высокая</strong>
                        <span>&gt; 80%</span>
                    </div>
                </div>
                <p class="analysis-note">Чем выше эффективность, тем меньше эпидемических недель и ниже пик заболеваемости.</p>
            </div>
        </div>
    </div>
</div>

<!-- блок: пример работы приложения -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🖥️ Пример работы приложения</h3>
            </div>
            <div class="panel-body">
                <div class="step-row">
                    <div class="step-card">
                        <h5>Шаг 1. Пространственные и временные параметры</h5>
                        <p>Задайте размер сетки n×n, общее число крыс и длительность симуляции.</p>
                        <div class="step-image">
                            <img src="/static/img/shag1.png" alt="Параметры пространства и времени" class="step-screenshot">
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <h5>Шаг 2. Заражение и перемещение</h5>
                        <p>Укажите вероятность заражения p_infect и вероятность перемещения p_move.</p>
                        <div class="step-image">
                            <img src="/static/img/shag2.png" alt="Параметры заражения" class="step-screenshot">
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <h5>Шаг 3. Параметры вакцинации</h5>
                        <p>Укажите день начала вакцинации и процент вакцинируемых крыс.</p>
                        <div class="step-image">
                            <img src="/static/img/shag3.png" alt="Параметры вакцинации" class="step-screenshot">
                        </div>
                    </div>
                </div>

                <div class="alert alert-success" style="margin-top: 20px; font-size: 14px;">
                    <strong>✅ Итог:</strong> После выполнения всех шагов вы получите полную картину распространения эпидемии, сможете оценить эффективность вакцинации и определить пороговые значения заболеваемости.
                </div>
            </div>
        </div>
    </div>
</div>

<!-- блок: расчётная панель -->
<div id="calculate" class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🧮 Расчётная панель</h3>
            </div>
            <div class="panel-body">
                <form action="/epidemic" method="post" id="calculationForm" novalidate>
                    <div class="row">
                        <!-- колонка 1: Пространство и время -->
                        <div class="col-md-4">
                            <h5>Пространство и время</h5>
                            
                            <div class="form-group" id="group-grid_size">
                                <label class="col-sm-12 control-label">Размер сетки n×n:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="1" name="grid_size" id="grid_size" class="form-control" value="8" required>
                                    <span class="help-block">Диапазон: 2–10</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-total_rats">
                                <label class="col-sm-12 control-label">Общее число крыс:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="1" name="total_rats" id="total_rats" class="form-control" value="64" required>
                                    <span class="help-block">Максимум: n² × 4</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-weeks">
                                <label class="col-sm-12 control-label">Длительность (недели):</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="1" name="weeks" id="weeks" class="form-control" value="52" required>
                                    <span class="help-block">Диапазон: 8–260</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 2: Заражение и перемещение -->
                        <div class="col-md-4">
                            <h5>Заражение и перемещение</h5>
                            
                            <div class="form-group" id="group-p_infect">
                                <label class="col-sm-12 control-label">Вероятность заражения:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="0.05" name="p_infect" id="p_infect" class="form-control" value="0.6" required>
                                    <span class="help-block">Диапазон: 0.1–0.9</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-p_move">
                                <label class="col-sm-12 control-label">Вероятность перемещения:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="0.05" name="p_move" id="p_move" class="form-control" value="0.5" required>
                                    <span class="help-block">Диапазон: 0.1–0.9</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 3: Вакцинация -->
                        <div class="col-md-4">
                            <h5>Вакцинация</h5>
                            
                            <div class="form-group" id="group-vacc_day">
                                <label class="col-sm-12 control-label">День начала вакцинации:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="1" name="vacc_day" id="vacc_day" class="form-control" value="56" required>
                                    <span class="help-block">Минимум: 56 (8 недель)</span>
                                </div>
                            </div>
                            
                            <div class="form-group" id="group-vacc_percent">
                                <label class="col-sm-12 control-label">Процент вакцинируемых крыс:</label>
                                <div class="col-sm-12" style="position: relative;">
                                    <input type="number" step="5" name="vacc_percent" id="vacc_percent" class="form-control" value="50" required>
                                    <span class="help-block">Диапазон: 1–100%</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- кнопка запуска -->
                    <div class="form-group">
                        <div class="col-sm-12">
                            <button type="submit" name="reset" value="false" class="btn btn-run" id="submitBtn">
                                ▶ Запустить расчёт
                            </button>
                            <button type="submit" name="reset" value="true" class="btn btn-run">
                                ⟳ Сброс данных
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- блок: визуализация матрицы -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🗺️ Визуализация матрицы</h3>
            </div>
            <div class="panel-body">
                <div class="matrix-layout">
                    <div class="matrix-wrapper">
                        <div class="matrix-container">
                            <table class="matrix-table">
                                <tbody>
                                    % if results and results.get('matrix_display'):
                                        % for i in range(results['n']):
                                            <tr>
                                                % for j in range(results['n']):
                                                    <td>
                                                        <div class="cell-content">
                                                            % for status in results['matrix_display'][i][j]:
                                                                % if status == 'S':
                                                                    <span class="stat-s">●</span>
                                                                % elif status == 'I':
                                                                    <span class="stat-i">●</span>
                                                                % elif status == 'R':
                                                                    <span class="stat-r">●</span>
                                                                % end
                                                            % end
                                                        </div>
                                                    </td>
                                                % end
                                            </tr>
                                        % end
                                    % else:
                                        % for i in range(10):
                                            <tr>
                                                % for j in range(10):
                                                    <td>
                                                        <div class="cell-content">
                                                            % if (i + j) % 3 == 0:
                                                                <span class="stat-s">●</span>
                                                            % elif (i + j) % 3 == 1:
                                                                <span class="stat-i">●</span>
                                                            % else:
                                                                <span class="stat-r">●</span>
                                                            % end
                                                        </div>
                                                    </td>
                                                % end
                                            </tr>
                                        % end
                                    % end
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="matrix-legend">
                        <div class="legend-title">Статусы</div>
                        <div class="legend-item">
                            <div class="legend-color color-s"></div>
                            <span class="legend-text">S (здоровые)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color color-i"></div>
                            <span class="legend-text">I (заражённые)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color color-r"></div>
                            <span class="legend-text">R (иммунные)</span>
                        </div>
                        
                        <div class="legend-divider"></div>
                        
                        <div class="legend-buttons">
                            <button class="btn btn-success btn-sm matrix-btn" disabled>▶ Старт</button>
                            <button class="btn btn-danger btn-sm matrix-btn" disabled>🔄 Сброс</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- блок: результаты симуляции -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📈 Результаты симуляции</h3>
            </div>
            <div class="panel-body">
                <div class="results-layout">
                    <div class="graph-container">
                        <div class="graph-placeholder">
                            <strong>📊 График динамики SIR</strong>
                            <div class="graph-description">
                                <span style="color: #2ecc71;">🟢 S (здоровые)</span> |
                                <span style="color: #e74c3c;">🔴 I (заражённые)</span> |
                                <span style="color: #f1c40f;">🟡 R (иммунные)</span>
                            </div>
                            <div class="graph-area">
                                % if results and results.get('graph'):
                                    <img src="{{results['graph']}}" alt="График динамики SIR" style="width:100%; border-radius:8px;">
                                % else:
                                    <svg width="100%" height="250" viewBox="0 0 600 250" preserveAspectRatio="none" style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 8px;">
                                        <text x="280" y="125" text-anchor="middle" fill="#999" font-size="14">Здесь будет график</text>
                                    </svg>
                                % end
                            </div>
                            <p class="graph-note">Ось X — недели, ось Y — количество крыс</p>
                        </div>
                    </div>
                    
                    <div class="results-container">
                        <div class="result-card">
                            <div class="result-title">🧪 Эпидемический порог</div>
                            % if results and results.get('threshold') is not None:
                                <div class="result-value" id="epidemic-threshold">{{results['threshold']}}</div>
                            % else:
                                <div class="result-value" id="epidemic-threshold">—</div>
                            % end
                            <div class="result-unit">заражённых в неделю</div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">💉 Эффективность вакцинации</div>
                            % if results and results.get('efficacy') is not None:
                                <div class="result-value" id="vaccine-efficacy">{{results['efficacy']}}%</div>
                            % else:
                                <div class="result-value" id="vaccine-efficacy">—</div>
                            % end
                            <div class="result-description">
                                <span class="efficiency-badge efficiency-low">Низкая &lt;50%</span>
                                <span class="efficiency-badge efficiency-medium">Средняя 50-80%</span>
                                <span class="efficiency-badge efficiency-high">Высокая &gt;80%</span>
                            </div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">📊 Пик заболеваемости</div>
                            <div class="result-compare">
                                <div class="compare-item">
                                    <span class="compare-label">Без вакцинации:</span>
                                    % if results and results.get('peak_without') is not None:
                                        <span class="compare-value" id="peak-without">{{results['peak_without']}} крыс</span>
                                        <span class="compare-unit">(неделя {{results['week_without']}})</span>
                                    % else:
                                        <span class="compare-value" id="peak-without">—</span>
                                    % end
                                </div>
                                <div class="compare-item">
                                    <span class="compare-label">С вакцинацией:</span>
                                    % if results and results.get('peak_with') is not None:
                                        <span class="compare-value" id="peak-with">{{results['peak_with']}} крыс</span>
                                        <span class="compare-unit">(неделя {{results['week_with']}})</span>
                                    % else:
                                        <span class="compare-value" id="peak-with">—</span>
                                    % end
                                </div>
                                <div class="compare-item">
                                    <span class="compare-label">Снижение пика:</span>
                                    % if results and results.get('reduction') is not None:
                                        <span class="compare-value reduction">{{results['reduction']}}%</span>
                                    % else:
                                        <span class="compare-value reduction">—</span>
                                    % end
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- JavaScript для валидации -->
<script>
// Правила валидации для эпидемии
const validationRules = {
    grid_size: { min: 2, max: 10, message: 'Размер сетки должен быть в диапазоне 2–10' },
    total_rats: { min: 1, max: 400, message: 'Число крыс должно быть в диапазоне 1–400' },
    weeks: { min: 8, max: 260, message: 'Длительность должна быть в диапазоне 8–260 недель' },
    p_infect: { min: 0.1, max: 0.9, message: 'Вероятность заражения должна быть в диапазоне 0.1–0.9' },
    p_move: { min: 0.1, max: 0.9, message: 'Вероятность перемещения должна быть в диапазоне 0.1–0.9' },
    vacc_day: { min: 56, max: 1820, message: 'День вакцинации должен быть не меньше 56 (8 недель)' },
    vacc_percent: { min: 1, max: 100, message: 'Процент вакцинации должен быть в диапазоне 1–100%' }
};

// Функция проверки одного поля
function validateField(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return true;
    
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

// Дополнительная проверка зависимостей
function validateDependencies() {
    let isValid = true;
    
    // Проверка: число крыс не больше максимума
    const gridSize = parseFloat(document.getElementById('grid_size')?.value || 8);
    const totalRats = parseFloat(document.getElementById('total_rats')?.value || 64);
    const maxRats = gridSize * gridSize * 4;
    
    if (totalRats > maxRats) {
        const formGroup = document.getElementById('group-total_rats');
        const inputWrapper = document.getElementById('total_rats')?.parentElement;
        if (inputWrapper) {
            const oldIcon = inputWrapper.querySelector('.error-icon');
            const oldTooltip = inputWrapper.querySelector('.error-tooltip');
            if (oldIcon) oldIcon.remove();
            if (oldTooltip) oldTooltip.remove();
            
            formGroup.classList.add('has-error');
            formGroup.classList.remove('has-success');
            
            const errorIcon = document.createElement('div');
            errorIcon.className = 'error-icon';
            errorIcon.innerHTML = '<span>⚠️</span>';
            
            const tooltip = document.createElement('div');
            tooltip.className = 'error-tooltip';
            tooltip.innerHTML = `⚠️ Число крыс не может превышать ${maxRats} (n² × 4)`;
            
            inputWrapper.appendChild(errorIcon);
            inputWrapper.appendChild(tooltip);
            isValid = false;
        }
    }
    
    // Проверка: день вакцинации не больше общей длительности
    const weeks = parseFloat(document.getElementById('weeks')?.value || 52);
    const vaccDay = parseFloat(document.getElementById('vacc_day')?.value || 56);
    const maxDay = weeks * 7;
    
    if (vaccDay > maxDay) {
        const formGroup = document.getElementById('group-vacc_day');
        const inputWrapper = document.getElementById('vacc_day')?.parentElement;
        if (inputWrapper) {
            const oldIcon = inputWrapper.querySelector('.error-icon');
            const oldTooltip = inputWrapper.querySelector('.error-tooltip');
            if (oldIcon) oldIcon.remove();
            if (oldTooltip) oldTooltip.remove();
            
            formGroup.classList.add('has-error');
            formGroup.classList.remove('has-success');
            
            const errorIcon = document.createElement('div');
            errorIcon.className = 'error-icon';
            errorIcon.innerHTML = '<span>⚠️</span>';
            
            const tooltip = document.createElement('div');
            tooltip.className = 'error-tooltip';
            tooltip.innerHTML = `⚠️ День вакцинации не может превышать ${maxDay} (всего дней симуляции)`;
            
            inputWrapper.appendChild(errorIcon);
            inputWrapper.appendChild(tooltip);
            isValid = false;
        }
    }
    
    return isValid;
}

// Проверка всех полей
function validateAllFields() {
    let isValid = true;
    for (const fieldId in validationRules) {
        if (!validateField(fieldId)) isValid = false;
    }
    if (!validateDependencies()) isValid = false;
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
        Исправьте поля с красной рамкой перед отправкой
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
            field.addEventListener('input', () => {
                validateField(fieldId);
                validateDependencies();
            });
            field.addEventListener('blur', () => {
                validateField(fieldId);
                validateDependencies();
            });
        }
    }
    
    const form = document.getElementById('calculationForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateAllFields()) {
                e.preventDefault();
                showErrorSummary();
                const firstError = document.querySelector('.has-error');
                if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }
    
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