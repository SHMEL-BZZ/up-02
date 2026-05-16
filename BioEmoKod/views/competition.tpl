% rebase('layout.tpl', title=title, year=year, active_page='competition')

<!-- специальный стиль для страницы Конкуренция видов -->
<link rel="stylesheet" type="text/css" href="/static/content/competition.css" />

<!-- Заголовок страницы -->
<div class="page-header">
    <h2>Модель «Конкуренция видов»</h2>
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
            <li><strong>Драка:</strong> случайный победитель, проигравший умирает (❌)</li>
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
                    <li><strong>Серых крыс</strong> — начальное количество серых крыс</li>
                    <li><strong>Белых крыс</strong> — начальное количество белых крыс</li>
                    <li><strong>Начальная рожь</strong> — количество единиц ржи на старте</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li><strong>Частота ржи (сек)</strong> — интервал появления новой ржи</li>
                    <li><strong>Новой ржи за раз</strong> — количество ржи при каждом появлении</li>
                    <li><strong>Максимум тактов</strong> — ограничение по времени симуляции</li>
                    <li><strong>Скорость</strong> — ускорение/замедление анимации</li>
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
                    <li><strong>▶ Старт</strong> — запускает автоматическую симуляцию</li>
                    <li><strong>⏸ Пауза</strong> — приостанавливает симуляцию</li>
                    <li><strong>🔄 Сброс</strong> — сбрасывает все параметры к начальным</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li><strong>⏩ Один такт</strong> — выполняет один шаг симуляции</li>
                    <li><strong>📎 Скачать CSV</strong> — экспортирует историю в CSV-файл</li>
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
        <p>По окончании симуляции вы можете сохранить отчёт:</p>
        <ul>
            <li>Нажмите кнопку <strong>«Скачать CSV»</strong></li>
            <li>Файл сохраняется с именем <code>competition_report_YYYYMMDD_HHMMSS.csv</code></li>
            <li>CSV содержит потактовую статистику и итоговый вердикт</li>
        </ul>
    </div>
</div>

<!-- СИМУЛЯТОР -->
<div id="simulator" class="model-card">
    <h2>🎮 Симулятор «Конкуренция видов»</h2>
    
    
    <div class="row">
        <div class="col-md-3"><label class = "stat-label">🗂️ Размер поля n</label><input type="number" id="fieldSize" class="form-control" value="8" min="2" max="10"></div>
        <div class="col-md-3"><label class = "stat-label">🐀 Серых крыс</label><input type="number" id="grayRats" class="form-control" value="6" min="0" max="99"></div>
        <div class="col-md-3"><label class = "stat-label">🐁 Белых крыс</label><input type="number" id="whiteRats" class="form-control" value="6" min="0" max="99"></div>
        <div class="col-md-3"><label class = "stat-label">🌾 Начальная рожь</label><input type="number" id="initialRye" class="form-control" value="8" min="1" max="99"></div>
        <div class="col-md-3"><label class = "stat-label">⏱️ Частота ржи (сек)</label><input type="number" id="ryeSpawnIntervalSec" class="form-control" value="6" min="2" max="100"></div>
        <div class="col-md-3"><label class = "stat-label">➕ Новой ржи за раз</label><input type="number" id="ryeSpawnCount" class="form-control" value="1" min="1" max="3"></div>
        <div class="col-md-3"><label class = "stat-label">⏲️ Максимум тактов</label><input type="number" id="maxTicks" class="form-control" value="150" min="10" max="1000"></div>
        <div class="col-md-3"><label class = "stat-label">⚡ Скорость</label>
            <input type="range" id="speedSlider" min="0.1" max="2" step="0.05" value="1" class="form-control">
            <span id="speedValue" class="stat-label">1.00</span>
        </div>
    </div>
    
    <div class="control-panel">
        <button class="control-btn" id="startBtn">▶ Старт</button>
        <button class="control-btn stop-btn" id="pauseBtn">⏸ Пауза</button>
        <button class="control-btn" id="resetBtn">🔄 Сброс</button>
        <button class="control-btn" id="stepBtn">⏩ Один такт</button>
        <button class="control-btn export-btn" id="exportCsvBtn">📎 Скачать CSV</button>
    </div>
    
    <div class="row">
        <div class="col-md-8">
            <div id="fieldGrid" class="field"></div>
        </div>
        <div class="col-md-4">
            <div class="stats-panel">
                <div class="stat-item"><div class="stat-label">⏱️ Такт</div><div class="stat-value" id="tickVal">0</div></div>
                <div class="stat-item"><div class="stat-label">🐀 Серые</div><div class="stat-value" id="grayVal">0</div></div>
                <div class="stat-item"><div class="stat-label">🐁 Белые</div><div class="stat-value" id="whiteVal">0</div></div>
                <div class="stat-item"><div class="stat-label">🌾 Рожь</div><div class="stat-value" id="ryeVal">0</div></div>
                <div class="stat-item"><div class="stat-label">⬜ Свободные</div><div class="stat-value" id="freeVal">0</div></div>
                <div class="stat-item"><div class="stat-label">⚔️ Драк</div><div class="stat-value" id="fightsTotal">0</div></div>
                <div class="stat-item"><div class="stat-label">🍼 Рождений</div><div class="stat-value" id="birthsTotal">0</div></div>
                <div class="stat-item"><div class="stat-label">💀 Смертей</div><div class="stat-value" id="deathsTotal">0</div></div>
            </div>
        </div>
    </div>
    
    <div class="chart-container">
    </div>
    
    <div class="formula-box">
        <strong>📐 Использованные формулы:</strong><br>
        dG/dt = r₁·G·(K₁ − G − α·W)/K₁ — скорость изменения серых крыс<br>
        dW/dt = r₂·W·(K₂ − W − β·G)/K₂ — скорость изменения белых крыс<br>
        K₁ = K₂ = floor(n²/2) — ёмкость среды для каждого вида<br>
        |h₁-h₂| &lt; 0.3 → мирный разбег, иначе драка
    </div>
</div>


