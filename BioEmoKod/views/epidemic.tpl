% rebase('layout.tpl', title=title, year=year)

<!-- Подключение уникальных стилей для страницы эпидемии -->
<link rel="stylesheet" type="text/css" href="/static/content/epidemic.css" />

<div class="page-header">
    <h2>Модель «Распространение эпидемии»</h2>
</div>

<!-- Кнопка перехода к расчётной панели -->
<div class="jump-button">
    <a href="#calculate" class="btn btn-jump">⬇ Перейти к расчётам</a>
</div>

<!-- теоретический блок -->
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

                    <!-- 3. Формулы расчёта (компактно) -->
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
                
                <!-- Ряд 1: Шаги 1, 2, 3 -->
                <div class="step-row">
                    <div class="step-card">
                        <h5>Шаг 1. Пространственные и временные параметры</h5>
                        <p>Задайте размер сетки n×n, общее число крыс и длительность симуляции.</p>
                        <div class="step-image">
                            <img src="/static/img/ввод1.png" alt="Параметры пространства и времени" class="step-screenshot">
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <h5>Шаг 2. Заражение и перемещение</h5>
                        <p>Укажите вероятность заражения p_infect и вероятность перемещения p_move.</p>
                        <div class="step-image">
                            <img src="/static/img/ввод2.png" alt="Параметры заражения" class="step-screenshot">
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <h5>Шаг 3. Параметры вакцинации</h5>
                        <p>Укажите день начала вакцинации и процент вакцинируемых крыс.</p>
                        <div class="step-image">
                            <img src="/static/img/ввод3.png" alt="Параметры вакцинации" class="step-screenshot">
                        </div>
                    </div>
                </div>

                <!-- Итоговое резюме -->
                <div class="alert alert-success" style="margin-top: 20px; font-size: 14px;">
                    <strong>✅ Итог:</strong> После выполнения всех шагов вы получите полную картину распространения эпидемии, сможете оценить эффективность вакцинации и определить пороговые значения заболеваемости.
                </div>

            </div>
        </div>
    </div>
</div>

<!-- блок: расчётная панель -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🧮 Расчётная панель</h3>
            </div>
            <div class="panel-body">
                <form action="/epidemic" method="post">
                    
                    <div class="row">
                        <!-- колонка 1: Пространство и время -->
                        <div class="col-md-4">
                            <h5>Пространство и время</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Размер сетки n×n:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="grid_size" class="form-control" value="8" min="2" max="10" required>
                                    <span class="help-block">n = 2..10</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Общее число крыс:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="total_rats" class="form-control" value="64" min="1" max="400" required>
                                    <span class="help-block">максимум n²·4</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Длительность (недели):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="weeks" class="form-control" value="52" min="8" max="260" required>
                                    <span class="help-block">8..260</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 2: Заражение и перемещение -->
                        <div class="col-md-4">
                            <h5>Заражение и перемещение</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Вероятность заражения:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.05" name="p_infect" class="form-control" value="0.6" min="0.1" max="0.9" required>
                                    <span class="help-block">0.1..0.9</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Вероятность перемещения:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.05" name="p_move" class="form-control" value="0.5" min="0.1" max="0.9" required>
                                    <span class="help-block">0.1..0.9</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 3: Вакцинация -->
                        <div class="col-md-4">
                            <h5>Вакцинация</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">День начала вакцинации:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="vacc_day" class="form-control" value="56" min="56" max="364" required>
                                    <span class="help-block">56..t·7 (максимум зависит от недель)</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label">Процент вакцинируемых крыс:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="5" name="vacc_percent" class="form-control" value="50" min="1" max="100" required>
                                    <span class="help-block">1%..100%</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- кнопка запуска -->
                    <div class="form-group">
                        <div class="col-sm-12">
                            <button type="submit" class="btn btn-run">
                                ▶ Запустить расчёт
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

                    <!-- Матрица -->
                    <div class="matrix-wrapper">
                        <div class="matrix-container">
                            <table class="matrix-table">
                                <tbody>
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
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Легенда -->
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
                        
                        <!-- Кнопки управления -->
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
                                <svg width="100%" height="250" viewBox="0 0 600 250" preserveAspectRatio="none" style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 8px;">
                                    <text x="280" y="125" text-anchor="middle" fill="#999" font-size="14">Здесь будет график</text>
                                </svg>
                            </div>
                            <p class="graph-note">Ось X — недели, ось Y — количество крыс</p>
                        </div>
                    </div>
                    
                    <!-- Результаты -->
                    <div class="results-container">
                        <div class="result-card">
                            <div class="result-title">🧪 Эпидемический порог</div>
                            <div class="result-value" id="epidemic-threshold">42</div>
                            <div class="result-unit">заражённых в неделю</div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">💉 Эффективность вакцинации</div>
                            <div class="result-value" id="vaccine-efficacy">67%</div>
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
                                    <span class="compare-value" id="peak-without">78 крыс</span>
                                    <span class="compare-unit">(неделя 6)</span>
                                </div>
                                <div class="compare-item">
                                    <span class="compare-label">С вакцинацией:</span>
                                    <span class="compare-value" id="peak-with">34 крыс</span>
                                    <span class="compare-unit">(неделя 9)</span>
                                </div>
                                <div class="compare-item">
                                    <span class="compare-label">Снижение пика:</span>
                                    <span class="compare-value reduction">56%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>