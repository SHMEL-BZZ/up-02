% rebase('layout.tpl', title='Конкуренция видов', year=year, active_page='competition')

% if auto and not extinct and tick < max_ticks:
    <meta http-equiv="refresh" content="{{speed}}; URL=/competition?auto=1&speed={{speed}}&n={{n}}&gray={{gray}}&white={{white}}&rye={{rye}}&rye_interval={{rye_interval}}&rye_spawn_count={{rye_spawn_count}}&max_ticks={{max_ticks}}">
% end

<link rel="stylesheet" type="text/css" href="/static/content/competition.css">

<!-- Заголовок страницы -->
<div class="page-header">
    <h2>Модель "Конкуренция видов"</h2>
</div>

<!-- навигация по странице-->
<div class="page-nav">
    <a href="#theory" class="nav-link">📖 Теория</a>
    <span class="nav-separator">|</span>
    <a href="#example" class="nav-link">🧪 Пример</a>
    <span class="nav-separator">|</span>
    <a href="#simulator" class="nav-link">🎮 Симулятор</a>
</div>

<!-- ТЕОРИЯ -->
<div id="theory" class="model-card">
    <h3>📖 Математическая модель конкуренции</h3>
    
    <p><strong>Классическая модель Лотки-Вольтерры для конкуренции двух видов:</strong></p>
    
    <div class="formula-box">
        <strong>Уравнение для серых крыс (G):</strong><br>
        dG/dt = r₁ · G · (K₁ − G − α · W) / K₁<br><br>
        <strong>Уравнение для белых крыс (W):</strong><br>
        dW/dt = r₂ · W · (K₂ − W − β · G) / K₂
    </div>
    
    <div class="formula-explanation">
        <h3>📐 Расшифровка параметров формулы:</h3>
        
        <div class="param-row">
            <div class="param-symbol"><strong>G(t)</strong></div>
            <div class="param-desc"><strong>Численность серых крыс</strong> — количество особей первого вида в момент времени t</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>W(t)</strong></div>
            <div class="param-desc"><strong>Численность белых крыс</strong> — количество особей второго вида в момент времени t</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>dG/dt</strong></div>
            <div class="param-desc"><strong>Скорость изменения серых крыс</strong> — на сколько изменится популяция серых за единицу времени</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>dW/dt</strong></div>
            <div class="param-desc"><strong>Скорость изменения белых крыс</strong> — на сколько изменится популяция белых за единицу времени</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>r₁, r₂</strong></div>
            <div class="param-desc"><strong>Скорость размножения</strong> — максимальная скорость роста популяции в благоприятных условиях</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>K₁, K₂</strong></div>
            <div class="param-desc"><strong>Ёмкость среды</strong> — максимальное количество крыс, которое может выдержать среда (K = n²/2)</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>α (альфа)</strong></div>
            <div class="param-desc"><strong>Коэффициент конкуренции</strong> — влияние белых крыс на серых (1 белая = α серых)</div>
        </div>
        <div class="param-row">
            <div class="param-symbol"><strong>β (бета)</strong></div>
            <div class="param-desc"><strong>Коэффициент конкуренции</strong> — влияние серых крыс на белых (1 серая = β белых)</div>
        </div>
    </div>
    
    <div class="formula-explanation">
        <h3>⚖️ Как работает модель Лотки-Вольтерры:</h3>
        <ul>
            <li><strong>Логистический рост:</strong> множитель (K − N)/K ограничивает рост из-за нехватки ресурсов</li>
            <li><strong>Конкуренция:</strong> члены α·W и β·G учитывают, что особи другого вида тоже потребляют ресурсы</li>
            <li><strong>Равновесие:</strong> популяции стабильны, когда dG/dt = 0 и dW/dt = 0</li>
            <li><strong>Исход конкуренции:</strong> если α > K₁/K₂ и β > K₂/K₁ — возможно сосуществование видов</li>
        </ul>
    </div>
    
    <div class="formula-explanation">
        <h3>🎮 Как это реализовано в симуляторе:</h3>
        <ul>
            <li><strong>Враждебность:</strong> случайный коэффициент h ∈ [0,1] у каждой крысы (аналог α и β)</li>
            <li><strong>Размножение:</strong> 2 крысы одного вида + рожь в клетке → новая крыса</li>
            <li><strong>Конфликт видов:</strong> |h₁-h₂| &lt; 0.3 → разбегаются, иначе драка</li>
            <li><strong>Драка:</strong> случайный победитель, проигравший умирает (💀)</li>
            <li><strong>Голод:</strong> крыса умирает через 10 тактов без еды</li>
            <li><strong>Рожь:</strong> съедается одной крысой или при размножении, появляется периодически</li>
        </ul>
    </div>
</div>

<!-- ПРИМЕР -->
<div id="example" class="model-card">
    <h2>🧪 Пример использования симулятора</h2>
    
    <!-- Шаг 1: Настройка параметров -->
    <div class="example-step">
        <h3>Шаг 1. Настройка параметров симуляции</h3>
        <p>Задайте начальные условия в панели параметров:</p>
        <div class="row">
            <div class="col-md-6">
                <ul>
                    <li><strong>Размер поля n</strong> — размер квадратного поля (от 2 до 10)</li>
                    <li><strong>Серых крыс</strong> — начальное количество серых крыс (не менее 2)</li>
                    <li><strong>Белых крыс</strong> — начальное количество белых крыс (не менее 2)</li>
                    <li><strong>Начальная рожь</strong> — количество единиц ржи на старте (от 1 до n²-4)</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li><strong>Частота ржи</strong> — интервал появления новой ржи (1-20)</li>
                    <li><strong>Новой ржи за раз</strong> — количество ржи при каждом появлении (1-5)</li>
                    <li><strong>Максимум тактов</strong> — ограничение по времени симуляции (10-500)</li>
                    <li><strong>Скорость</strong> — ускорение/замедление анимации (0.1-2.0 сек)</li>
                </ul>
            </div>
        </div>
        <div class="screenshot">
            <img src="/static/img/ex1.jpg" alt="Настройка параметров симуляции" class="img-responsive screenshot-img">
            <div class="screenshot-caption">Рис. 1 — Панель ввода параметров</div>
        </div>
    </div>
    
     <!-- Шаг 2: Управление симуляцией -->
    <div class="example-step">
        <h3>Шаг 2. Управление симуляцией</h3>
        <p>Кнопки управления позволяют контролировать ход симуляции:</p>
        <div class="row">
            <div class="col-md-6">
                <ul>
                    <li><strong>▶ Авто / ⏸ Стоп</strong> — запускает или останавливает автоматическую симуляцию</li>
                    <li><strong>🔄 Сброс</strong> — сбрасывает все параметры к начальным</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li><strong>📊 График</strong> — показывает график динамики популяций</li>
                    <li><strong>💾 CSV</strong> — экспортирует историю в CSV-файл</li>
                </ul>
            </div>
        </div>
        <div class="screenshot">
            <img src="/static/img/ex2.jpg" alt="Кнопки управления симуляцией" class="img-responsive screenshot-img">
            <div class="screenshot-caption">Рис. 2 — Панель управления симуляцией</div>
        </div>
    </div>
    
    <!-- Шаг 3: Наблюдение за симуляцией -->
    <div class="example-step">
        <h3>Шаг 3. Наблюдение за процессом</h3>
        <p>В процессе симуляции вы можете наблюдать:</p>
        <div class="row">
            <div class="col-md-6">
                <ul>
                    <li><strong>Игровое поле</strong> — клетки с крысами 🐀🐁, рожью 🌾</li>
                    <li><strong>Статистику в реальном времени</strong> — такт, количество крыс, ржи</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li><strong>Счётчики событий</strong> — драки, рождения, смерти</li>
                    <li><strong>График динамики</strong> — изменение численности популяций</li>
                </ul>
            </div>
        </div>
        <div class="screenshot">
            <img src="/static/img/ex3.jpg" alt="Отображение симуляции и статистики" class="img-responsive screenshot-img">
            <div class="screenshot-caption">Рис. 3 — Поле симуляции и панель статистики</div>
        </div>
    </div>
    
    <!-- Шаг 4: Экспорт результатов -->
    <div class="example-step">
        <h3>Шаг 4. Экспорт результатов</h3>
        <p>После генерации графика вы можете сохранить результаты:</p>
        <ul>
            <li>Нажмите кнопку <strong>💾 CSV</strong> для сохранения данных симуляции</li>
            <li>Нажмите кнопку <strong>📸 Сохранить график</strong> для скачивания графика в PNG</li>
        </ul>
    </div>
</div>

<!-- СИМУЛЯТОР -->
<div id="simulator" class="model-card">
    <h2>🎮 Симулятор</h2>
    
    <form method="POST" action="/competition" id="simulationForm">
        <!-- Панель параметров -->
        <div class="params-grid">
            <div class="param-group">
                <label>🗂️ Размер поля n</label>
                <input type="number" name="n" value="{{n}}" min="2" max="10" step="1" required>
            </div>
            <div class="param-group">
                <label>🐀 Серых крыс</label>
                <input type="number" name="gray" value="{{gray}}" min="2" required>
            </div>
            <div class="param-group">
                <label>🐁 Белых крыс</label>
                <input type="number" name="white" value="{{white}}" min="2" required>
            </div>
            <div class="param-group">
                <label>🌾 Начальная рожь</label>
                <input type="number" name="rye" value="{{rye}}" min="1" required>
            </div>
            <div class="param-group">
                <label>⏱️ Частота ржи</label>
                <input type="number" name="rye_interval" value="{{rye_interval}}" min="1" max="20" required>
            </div>
            <div class="param-group">
                <label>➕ Новой ржи за раз</label>
                <input type="number" name="rye_spawn_count" value="{{rye_spawn_count}}" min="1" max="5" required>
            </div>
            <div class="param-group">
                <label>⏲️ Максимум тактов</label>
                <input type="number" name="max_ticks" value="{{max_ticks}}" min="1" max="200" required>
            </div>
            <div class="param-group">
                <label>⚡ Скорость (сек)</label>
                <input type="number" name="speed" value="{{speed}}" step="0.1" min="0.1" max="2.0" required>
            </div>
        </div>
        
        <!-- Кнопки управления -->
        <div class="control-panel">
            % if auto:
                <button type="submit" name="action" value="auto_off" class="control-btn stop-btn">⏸ Стоп</button>
            % else:
                <button type="submit" name="action" value="auto_on" class="control-btn" {% if extinct %}disabled{% end %}>▶ Авто</button>
            % end
            <button type="submit" name="action" value="reset" class="control-btn stop-btn">🔄 Сброс</button>
            <button type="submit" name="action" value="chart" class="control-btn">📊 График</button>
            <button type="submit" name="action" value="csv" class="control-btn export-btn">💾 CSV</button>
            <button type="submit" name="action" value="randomize" class="control-btn randomize-btn">🎲 Генерация значений</button>
        </div>
    </form>
    
    <!-- Игровое поле и статистика -->
    <div class="game-area">
        <div class="field-container">
            <h3>Игровое поле (Такт: {{tick}})</h3>
            <div class="field" style="grid-template-columns: repeat({{int(n)}}, 1fr);">
                % for i in range(int(n)):
                    % for j in range(int(n)):
                        % if i < len(cell_class) and j < len(cell_class[i]):
                            <div class="cell {{cell_class[i][j]}}">{{!cell_content[i][j]}}</div>
                        % else:
                            <div class="cell cell-empty">⬜</div>
                        % end
                    % end
                % end
            </div>
        </div>
        
        <div class="stats-container">
            <h3>Статистика</h3>
            <div class="stats-panel">
                <div class="stat-item">
                    <div class="stat-label">⏱️ Такт</div>
                    <div class="stat-value">{{tick}}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">🐀 Серые</div>
                    <div class="stat-value">{{gray_count}}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">🐁 Белые</div>
                    <div class="stat-value">{{white_count}}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">🌾 Рожь</div>
                    <div class="stat-value">{{rye_count}}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">⚔️ Драк</div>
                    <div class="stat-value">{{fights}}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">💀 Смертей</div>
                    <div class="stat-value">{{deaths}}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- График и кнопки экспорта -->
    % if chart:
        <div class="chart-container">
            <h3>📈 График динамики популяций</h3>
            <img src="{{chart}}" alt="График динамики популяций" class="chart-image" id="populationChart">
            
            <!-- Кнопки экспорта под графиком -->
            <div class="export-buttons">
                <form method="POST" action="/competition/export/csv" style="display: inline;">
                    <button type="submit" class="control-btn export-btn">💾 Экспорт CSV</button>
                </form>
                <form method="POST" action="/competition/export/chart" style="display: inline;">
                    <input type="hidden" name="chart_path" value="{{chart}}">
                    <button type="submit" class="control-btn export-btn">📸 Сохранить график (PNG)</button>
                </form>
            </div>
        </div>
    % end
    
    <!-- Сообщение об успехе -->
    % if csv_msg:
        <div class="success-message">✅ {{csv_msg}}</div>
    % end
    
    <!-- Результаты и аналитика -->
    <div class="results-analytics">
        <!-- Верхняя панель с вердиктом -->
        <div class="verdict-panel {{'verdict-extinct' if extinct else ''}}">
            <div class="verdict-icon">
                % if extinct:
                    💀
                % elif gray_count > 0 and white_count > 0:
                    🤝
                % elif gray_count == 0 and white_count > 0:
                    🏆
                % elif white_count == 0 and gray_count > 0:
                    🏆
                % else:
                    ❓
                % end
            </div>
            <div class="verdict-text">{{verdict}}</div>
        </div>
        
        <div class="two-columns">
            <!-- ЛЕВАЯ КОЛОНКА: Модель Лотки-Вольтерры -->
            <div class="lotka-card">
                <div class="card-header">
                    <span class="card-icon">📊</span>
                    <h3>Модель Лотки-Вольтерры</h3>
                </div>
                
                <!-- Параметры модели -->
                <div class="params-section">
                    <div class="param-card">
                        <div class="param-name">Ёмкость среды (K)</div>
                        <div class="param-value">K = n²/2 = <strong>{{K}}</strong></div>
                        <div class="param-desc">максимальное количество крыс одного вида</div>
                    </div>
                    
                    <div class="param-card">
                        <div class="param-name">Коэффициент α</div>
                        <div class="param-value"><strong>{{alpha}}</strong></div>
                        <div class="param-desc">влияние белых крыс на серых</div>
                    </div>
                    
                    <div class="param-card">
                        <div class="param-name">Коэффициент β</div>
                        <div class="param-value"><strong>{{beta}}</strong></div>
                        <div class="param-desc">влияние серых крыс на белых</div>
                    </div>
                </div>
                
                <!-- Анализ конкуренции -->
                <div class="analysis-section">
                    <div class="analysis-title">🔍 Анализ конкуренции</div>
                    % if extinct:
                        % if gray_count == 0 and white_count == 0:
                            <div class="analysis-result extinct-full">
                                <span class="result-icon">💀</span>
                                <span>Полное вымирание - оба вида исчезли</span>
                            </div>
                        % elif gray_count == 0:
                            <div class="analysis-result white-win">
                                <span class="result-icon">🏆</span>
                                <span>Победа белых крыс - серые полностью вытеснены</span>
                            </div>
                        % elif white_count == 0:
                            <div class="analysis-result gray-win">
                                <span class="result-icon">🏆</span>
                                <span>Победа серых крыс - белые полностью вытеснены</span>
                            </div>
                        % else:
                            <div class="analysis-result ongoing">
                                <span class="result-icon">⚖️</span>
                                <span>Конкуренция продолжается</span>
                            </div>
                        % end
                    % else:
                        % if alpha < 1 and beta < 1:
                            <div class="analysis-result coexistence">
                                <span class="result-icon">🤝</span>
                                <span>Возможно сосуществование видов (оба коэффициента &lt; 1)</span>
                            </div>
                        % elif alpha > 1 and beta > 1:
                            <div class="analysis-result competition">
                                <span class="result-icon">⚔️</span>
                                <span>Конкуренция приведёт к вытеснению одного вида</span>
                            </div>
                        % elif alpha > 1:
                            <div class="analysis-result white-advantage">
                                <span class="result-icon">🐁</span>
                                <span>Белые крысы имеют преимущество (α &gt; 1)</span>
                            </div>
                        % elif beta > 1:
                            <div class="analysis-result gray-advantage">
                                <span class="result-icon">🐀</span>
                                <span>Серые крысы имеют преимущество (β &gt; 1)</span>
                            </div>
                        % else:
                            <div class="analysis-result neutral">
                                <span class="result-icon">⚖️</span>
                                <span>Нестабильное равновесие - исход неопределён</span>
                            </div>
                        % end
                    % end
                </div>
                
                <!-- Точка равновесия -->
                <div class="equilibrium-section">
                    <div class="equilibrium-title">📐 Точка равновесия</div>
                    <div class="equilibrium-formula">
                        G* = K·(1-α)/(1-α·β) = <strong>{{g_star}}</strong><br>
                        W* = K·(1-β)/(1-α·β) = <strong>{{w_star}}</strong>
                    </div>
                    % if g_star > 0 and w_star > 0:
                        <div class="equilibrium-note">
                            ⚖️ При достижении равновесия:<br>
                            🐀 Серых ≈ {{g_star}} | 🐁 Белых ≈ {{w_star}}
                        </div>
                    % end
                </div>
                
                <!-- Дополнительная информация -->
                <details class="details-info">
                    <summary>📖 Подробнее о модели Лотки-Вольтерры</summary>
                    <div class="details-content">
                        <p><strong>Условия сосуществования:</strong><br>
                        α &lt; K₁/K₂ и β &lt; K₂/K₁ → возможно сосуществование видов</p>
                        <p><strong>Текущие значения:</strong><br>
                        K₁/K₂ = 1.0 | K₂/K₁ = 1.0</p>
                        <p><strong>Прогноз:</strong>
                        % if alpha < 1 and beta < 1:
                            Оба вида могут сосуществовать в долгосрочной перспективе
                        % elif alpha > 1:
                            Белые крысы имеют конкурентное преимущество
                        % elif beta > 1:
                            Серые крысы имеют конкурентное преимущество
                        % else:
                            Исход зависит от начальных условий и случайных факторов
                        % end
                        </p>
                    </div>
                </details>
            </div>
            
            <!-- ПРАВАЯ КОЛОНКА: Статистика и формулы -->
            <div class="stats-card">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h3>Статистика симуляции</h3>
                </div>
                
                <!-- Текущие показатели -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">⏱️</div>
                        <div class="stat-info">
                            <div class="stat-label">Такт</div>
                            <div class="stat-number">{{tick}}</div>
                        </div>
                    </div>
                    <div class="stat-card gray">
                        <div class="stat-icon">🐀</div>
                        <div class="stat-info">
                            <div class="stat-label">Серые крысы</div>
                            <div class="stat-number">{{gray_count}}</div>
                        </div>
                    </div>
                    <div class="stat-card white">
                        <div class="stat-icon">🐁</div>
                        <div class="stat-info">
                            <div class="stat-label">Белые крысы</div>
                            <div class="stat-number">{{white_count}}</div>
                        </div>
                    </div>
                    <div class="stat-card rye">
                        <div class="stat-icon">🌾</div>
                        <div class="stat-info">
                            <div class="stat-label">Рожь</div>
                            <div class="stat-number">{{rye_count}}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Счётчики событий -->
                <div class="events-section">
                    <div class="events-title">⚡ События за всё время</div>
                    <div class="events-grid">
                        <div class="event-item">
                            <span class="event-icon">⚔️</span>
                            <span class="event-count">{{fights}}</span>
                            <span class="event-label">Драк</span>
                        </div>

                        <div class="event-item">
                            <span class="event-icon">💀</span>
                            <span class="event-count">{{deaths}}</span>
                            <span class="event-label">Смертей</span>
                        </div>
                    </div>
                </div>
                
                <!-- Использованные формулы -->
                <div class="formulas-section">
                    <div class="formulas-title">📐 Использованные формулы</div>
                    <div class="formulas-content">
                        <div class="formula-item">
                            <span class="formula-name">Серые крысы:</span>
                            dG/dt = r₁·G·(K − G − α·W)/K
                        </div>
                        <div class="formula-item">
                            <span class="formula-name">Белые крысы:</span>
                            dW/dt = r₂·W·(K − W − β·G)/K
                        </div>
                        <div class="formula-item">
                            <span class="formula-name">Конфликт:</span>
                            |h₁-h₂| &lt; 0.3 → мирный разбег, иначе драка
                        </div>
                        <div class="formula-item">
                            <span class="formula-name">Голод:</span>
                            крыса умирает через 10 тактов без еды
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>