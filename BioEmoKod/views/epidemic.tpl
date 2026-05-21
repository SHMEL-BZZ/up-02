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
                                    <h5>Эпидемический порог</h5>
                                    <div class="formula-box formula-box-green">
                                        <p class="formula-text">X̄ = (X₁+...+X₈)/8</p>
                                        <p class="formula-text">σ = √[Σ(Xᵢ-X̄)²/7]</p>
                                        <p class="formula-text">X<sub>порог</sub> = X̄ + 2,507·σ</p>
                                    </div>
                                    <p class="formula-note">* на основе первых 8 недель (коэф. Стьюдента)</p>
                                </div>

                                <div class="formula-compact">
                                    <h5>Эффективность вакцинации</h5>
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
                <form action="/epidemic" method="post" id="calculationForm">
                    <div class="row">
                        <!-- колонка 1: Пространство и время -->
                        <div class="col-md-4">
                            <h5>Пространство и время</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Размер сетки n×n (2–10):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="grid_size" class="form-control" value="{{form_values.get('grid_size', '8')}}">
                                    % if field_errors.get('grid_size'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['grid_size']}}</div>
                                    % end
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Общее число крыс (2–n²×4):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="total_rats" class="form-control" value="{{form_values.get('total_rats', '64')}}">
                                    % if field_errors.get('total_rats'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['total_rats']}}</div>
                                % end
                                </div>
                            </div>
                            
                            <div class="form-group">
                               <label class="col-sm-12 control-label">Длительность, недели (8–260):</label>
                               <div class="col-sm-12">
                                    <input type="number" step="1" name="weeks" class="form-control" value="{{form_values.get('weeks', '52')}}">
                                    % if field_errors.get('weeks'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['weeks']}}</div>
                                    % end
                                </div>
                            </div>
                        </div>

                        <!-- колонка 2: Заражение и перемещение -->
                        <div class="col-md-4">
                            <h5>Заражение и перемещение</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Вероятность заражения (0.1–0.9):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.1" name="p_infect" class="form-control" value="{{form_values.get('p_infect', '0.6')}}">
                                    % if field_errors.get('p_infect'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['p_infect']}}</div>
                                    % end
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Вероятность перемещения (0.1–0.9):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.1" name="p_move" class="form-control" value="{{form_values.get('p_move', '0.5')}}">
                                    % if field_errors.get('p_move'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['p_move']}}</div>
                                    % end
                                </div>
                            </div>
                        </div>

                        <!-- колонка 3: Вакцинация -->
                        <div class="col-md-4">
                            <h5>Вакцинация</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">День начала вакцинации (≥56):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="vacc_day" class="form-control" value="{{form_values.get('vacc_day', '56')}}">
                                    % if field_errors.get('vacc_day'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['vacc_day']}}</div>
                                    % end
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Процент вакцинируемых крыс (1–100):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="vacc_percent" class="form-control" value="{{form_values.get('vacc_percent', '50')}}">
                                    % if field_errors.get('vacc_percent'):
                                    <div class="help-block" style="color: #e74c3c;">⚠️ {{field_errors['vacc_percent']}}</div>
                                    % end
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- кнопка запуска и сброса -->
                    <div class="form-group">
                        <div class="col-sm-12">
                            <button type="submit" name="reset" value="false" class="btn btn-run">
                                ▶ Запустить расчёт
                            </button>
                            <button type="submit" name="reset" value="true" class="btn btn-run" id="runButton">
                                ⟳ Сброс данных
                            </button>
                            <button type="submit" name="random" value="true" class="btn btn-run">
                                🎲 Генерация значений
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

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
                                <tbody id="matrix-body">
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
                        
                        <!-- Ползунок для выбора дня -->
                        <div class="slider-container">
                            <label>📅 День:</label>
                            <input type="range" id="daySlider" min="0" max="0" value="0" step="1" style="width: 100%;">
                            <span id="dayValue" style="font-size: 11px; display: block; text-align: center;">0</span>
                        </div>
                        
                        <div class="legend-divider"></div>
                        
                        <!-- Кнопки управления анимацией -->
                        <div class="legend-buttons">
                            <button class="btn btn-success btn-sm matrix-btn" id="btnPlay">▶ Старт</button>
                            <button class="btn btn-danger btn-sm matrix-btn" id="btnPause" style="display: none;">⏸ Пауза</button>
                            <button class="btn btn-warning btn-sm matrix-btn" id="btnReset">🔄 Сброс</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- блок: результаты симуляции -->
% if defined('results') and results:
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📈 Результаты симуляции</h3>
            </div>
            <div class="panel-body">
                <div class="results-layout">
                    <!-- SIR график -->
                    <div class="graph-container">
                        <div class="graph-placeholder">
                            <strong>📊 График динамики SIR</strong>
                            <div class="graph-description">
                                <span style="color: #2ecc71;">🟢 S (здоровые)</span> |
                                <span style="color: #e74c3c;">🔴 I (заражённые)</span> |
                                <span style="color: #f1c40f;">🟡 R (иммунные)</span>
                            </div>
                            <div class="graph-area">
                                % if results.get('graph'):
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
                            <div class="result-value">{{results.get('threshold', '—')}}</div>
                            <div class="result-unit">заражённых в неделю</div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">💉 Эффективность вакцинации</div>
                            <div class="result-value">{{results.get('efficacy', '—')}}%</div>
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
                                    <span class="compare-value">{{results.get('peak_without', '—')}} крыс</span>
                                    <span class="compare-unit">(неделя {{results.get('week_without', '—')}})</span>
                                </div>
                                <div class="compare-item">
                                    <span class="compare-label">С вакцинацией:</span>
                                    <span class="compare-value">{{results.get('peak_with', '—')}} крыс</span>
                                    <span class="compare-unit">(неделя {{results.get('week_with', '—')}})</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
               <!-- Кнопки экспорта -->
                <div class="export-buttons">
                    <form action="/epidemic/export/csv" method="post" style="display: inline;">
                        <!-- Передаём текущие параметры в скрытых полях -->
                        <input type="hidden" name="grid_size" value="{{form_values.get('grid_size', '8')}}">
                        <input type="hidden" name="total_rats" value="{{form_values.get('total_rats', '64')}}">
                        <input type="hidden" name="weeks" value="{{form_values.get('weeks', '52')}}">
                        <input type="hidden" name="p_infect" value="{{form_values.get('p_infect', '0.6')}}">
                        <input type="hidden" name="p_move" value="{{form_values.get('p_move', '0.5')}}">
                        <input type="hidden" name="vacc_day" value="{{form_values.get('vacc_day', '56')}}">
                        <input type="hidden" name="vacc_percent" value="{{form_values.get('vacc_percent', '50')}}">
                        <button type="submit" class="btn btn-export-csv">
                            Экспорт данных в CSV
                        </button>
                    </form>
    
                    <form action="/epidemic/export/graph" method="post" style="display: inline;">
                        <!-- Передаём текущие параметры в скрытых полях -->
                        <input type="hidden" name="grid_size" value="{{form_values.get('grid_size', '8')}}">
                        <input type="hidden" name="total_rats" value="{{form_values.get('total_rats', '64')}}">
                        <input type="hidden" name="weeks" value="{{form_values.get('weeks', '52')}}">
                        <input type="hidden" name="p_infect" value="{{form_values.get('p_infect', '0.6')}}">
                        <input type="hidden" name="p_move" value="{{form_values.get('p_move', '0.5')}}">
                        <input type="hidden" name="vacc_day" value="{{form_values.get('vacc_day', '56')}}">
                        <input type="hidden" name="vacc_percent" value="{{form_values.get('vacc_percent', '50')}}">
                        <button type="submit" class="btn btn-export-png">
                            Экспорт графика
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
% end

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные истории из results
    var historyMatrices = {{! results.get('history_matrices', '[]') if results else '[]' }};
    var totalDays = {{ results.get('total_days', 0) if results else 0 }};
    
    // Если нет данных для анимации — не инициализируем анимацию (оставляем заглушку)
    if (!historyMatrices || historyMatrices.length === 0) {
        console.log('Нет данных для анимации, оставляем статическую матрицу');
        return;
    }
    
    console.log('History matrices length:', historyMatrices.length);
    console.log('Total days:', totalDays);
    
    var currentIndex = totalDays;
    var animationInterval = null;
    var isPlaying = false;
    
    // Элементы управления
    var slider = document.getElementById('daySlider');
    var dayValue = document.getElementById('dayValue');
    var btnPlay = document.getElementById('btnPlay');
    var btnPause = document.getElementById('btnPause');
    var btnReset = document.getElementById('btnReset');
    var matrixBody = document.getElementById('matrix-body');
    
    // Устанавливаем максимальное значение слайдера
    if (slider) {
        slider.max = totalDays;
        slider.value = totalDays;
        if (dayValue) dayValue.innerText = 'День: ' + totalDays;
    }
    
    // Функция обновления матрицы по индексу
    function updateMatrix(dayIndex) {
        if (!historyMatrices[dayIndex]) return;
        
        var matrix = historyMatrices[dayIndex];
        var html = '';
        
        for (var i = 0; i < matrix.length; i++) {
            html += '<tr>';
            for (var j = 0; j < matrix[i].length; j++) {
                html += '<td><div class="cell-content">';
                var statuses = matrix[i][j];
                for (var k = 0; k < statuses.length; k++) {
                    var status = statuses[k];
                    if (status === 'S') {
                        html += '<span class="stat-s">●</span>';
                    } else if (status === 'I') {
                        html += '<span class="stat-i">●</span>';
                    } else if (status === 'R') {
                        html += '<span class="stat-r">●</span>';
                    }
                }
                html += '</div></td>';
            }
            html += '</tr>';
        }
        
        if (matrixBody) matrixBody.innerHTML = html;
        
        if (slider) slider.value = dayIndex;
        if (dayValue) dayValue.innerText = 'День: ' + dayIndex;
        
        currentIndex = dayIndex;
    }
    
    function startAnimation() {
        if (animationInterval) clearInterval(animationInterval);
        isPlaying = true;
        
        if (currentIndex >= totalDays) {
            currentIndex = 0;
            updateMatrix(currentIndex);
        }
        
        if (btnPlay) btnPlay.style.display = 'none';
        if (btnPause) btnPause.style.display = 'inline-block';
        
        animationInterval = setInterval(function() {
            if (currentIndex < totalDays) {
                currentIndex++;
                updateMatrix(currentIndex);
            } else {
                stopAnimation();
            }
        }, 200);
    }
    
    function stopAnimation() {
        if (animationInterval) {
            clearInterval(animationInterval);
            animationInterval = null;
        }
        isPlaying = false;
        
        if (btnPlay) btnPlay.style.display = 'inline-block';
        if (btnPause) btnPause.style.display = 'none';
    }
    
    function resetAnimation() {
        stopAnimation();
        currentIndex = totalDays;
        updateMatrix(totalDays);
    }
    
    // Привязываем события
    if (btnPlay) btnPlay.onclick = startAnimation;
    if (btnPause) btnPause.onclick = stopAnimation;
    if (btnReset) btnReset.onclick = resetAnimation;
    
    if (slider) {
        slider.oninput = function() {
            stopAnimation();
            updateMatrix(parseInt(this.value));
        };
    }
    
    // Инициализируем матрицу последним днём
    if (historyMatrices.length > 0 && totalDays > 0) {
        updateMatrix(totalDays);
    }
});
</script>