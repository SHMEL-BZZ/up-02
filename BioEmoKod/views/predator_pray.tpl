% rebase('layout.tpl', title=title, year=year)

<!-- специальный стиль для страницы Модель хищник-жертва -->
<head>
    <link rel="stylesheet" type="text/css" href="/static/content/predator_pray.css" />
</head>

<div class="page-header">
    <h2>{{ title }}.</h2>
</div>

<!-- ОСНОВНОЙ КОНТЕЙНЕР С FLEX ДЛЯ ВЫРАВНИВАНИЯ ВЫСОТЫ -->
<div class="row equal-height-row">
    <!-- ЛЕВАЯ КОЛОНКА: ТЕОРИЯ -->
    <div class="col-md-5">
        <div class="panel panel-info theory-panel">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📖 Теоретические сведения</h3>
            </div>
            <div class="panel-body">
                
                <!-- Раскрывающийся блок 1: Описание модели -->
                <div class="panel-group" id="accordion">
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

                    <!-- Раскрывающийся блок 2: Система уравнений -->
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

                    <!-- Раскрывающийся блок 3: Равновесие и устойчивость -->
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

                    <!-- Раскрывающийся блок 4: Примеры -->
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
                                    <li><em>Результат:</em> циклические колебания численности</li>
                                </ul>
                                <p><strong>Пример 2. Вымирание хищников:</strong></p>
                                <ul>
                                    <li>α = 0.5, c = 0.01, β = 1.2, d = 0.01</li>
                                    <li>x₀ = 30, y₀ = 5</li>
                                    <li><em>Результат:</em> хищники вымирают из-за высокой смертности</li>
                                </ul>
                                <p><strong>Пример 3. Вымирание жертв:</strong></p>
                                <ul>
                                    <li>α = 0.4, c = 0.08, β = 0.5, d = 0.01</li>
                                    <li>x₀ = 10, y₀ = 30</li>
                                    <li><em>Результат:</em> жертвы истребляются хищниками</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Раскрывающийся блок 5: Литература -->
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

    <!-- ПРАВАЯ КОЛОНКА: РАСЧЁТНАЯ ПАНЕЛЬ -->
    <div class="col-md-7">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🧮 Расчётная панель</h3>
            </div>
            <div class="panel-body">
                <form action="/predator_pray" method="post" class="form-horizontal">
                    
                    <!-- Начальные условия -->
                    <h4 class="text-center">📌 Начальные условия</h4>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">x₀ (численность жертв):</label>
                        <div class="col-sm-7">
                            <input type="number" step="any" name="x0" class="form-control" value="50" required>
                            <span class="help-block">Диапазон: 10–100</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">y₀ (численность хищников):</label>
                        <div class="col-sm-7">
                            <input type="number" step="any" name="y0" class="form-control" value="20" required>
                            <span class="help-block">Диапазон: 1–50</span>
                        </div>
                    </div>

                    <hr>

                    <!-- Параметры модели -->
                    <h4 class="text-center">⚙️ Параметры модели</h4>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">α (рождаемость жертв):</label>
                        <div class="col-sm-7">
                            <input type="number" step="0.01" name="alpha" class="form-control" value="0.8" required>
                            <span class="help-block">Диапазон: 0.4–1.5</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">c (эффективность охоты):</label>
                        <div class="col-sm-7">
                            <input type="number" step="0.01" name="c" class="form-control" value="0.04" required>
                            <span class="help-block">Диапазон: 0.01–0.06</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">β (смертность хищников):</label>
                        <div class="col-sm-7">
                            <input type="number" step="0.01" name="beta" class="form-control" value="0.6" required>
                            <span class="help-block">Диапазон: 0.4–1.5</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">d (вклад жертвы в рост хищников):</label>
                        <div class="col-sm-7">
                            <input type="number" step="0.01" name="d" class="form-control" value="0.02" required>
                            <span class="help-block">Диапазон: 0.01–0.06</span>
                        </div>
                    </div>

                    <hr>

                    <!-- Параметры симуляции -->
                    <h4 class="text-center">⏱️ Параметры симуляции</h4>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">T (длительность, лет):</label>
                        <div class="col-sm-7">
                            <input type="number" step="1" name="T" class="form-control" value="50" required>
                            <span class="help-block">Диапазон: 5–50</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-5 control-label">N (количество шагов):</label>
                        <div class="col-sm-7">
                            <input type="number" step="100" name="N" class="form-control" value="1000" required>
                            <span class="help-block">Диапазон: 200–10000</span>
                        </div>
                    </div>

                    <hr>

                    <!-- Кнопка запуска -->
                    <div class="form-group">
                        <div class="col-sm-offset-3 col-sm-6">
                            <button type="submit" class="btn btn-success btn-block">▶ Запустить расчёт</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Результаты расчёта (если есть) -->
% if defined('results') and results:
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-success">
            <div class="panel-heading">
                <h3 class="panel-title text-center">📈 Результаты моделирования</h3>
            </div>
            <div class="panel-body">
                <div class="row">
                    <div class="col-md-6">
                        <h4 class="text-center">Динамика численности во времени</h4>
                        <img src="/static/temp/{{ results.get('plot_time', '') }}" class="img-responsive img-thumbnail" alt="График динамики">
                    </div>
                    <div class="col-md-6">
                        <h4 class="text-center">Фазовый портрет</h4>
                        <img src="/static/temp/{{ results.get('plot_phase', '') }}" class="img-responsive img-thumbnail" alt="Фазовый портрет">
                    </div>
                </div>
                
                <hr>
                
                <div class="row">
                    <div class="col-md-12">
                        <h4 class="text-center">📊 Анализ результатов</h4>
                        <div class="well">
                            <p><strong>Равновесная численность жертв (x*):</strong> {{ results.get('x_star', 'Н/Д') }}</p>
                            <p><strong>Равновесная численность хищников (y*):</strong> {{ results.get('y_star', 'Н/Д') }}</p>
                            <p><strong>Расчётный период колебаний:</strong> {{ results.get('period', 'Н/Д') }} лет</p>
                            <p><strong>Тип устойчивости:</strong> {{ results.get('stability', 'Н/Д') }}</p>
                        </div>
                    </div>
                </div>
                
                <!-- Кнопки экспорта -->
                <div class="row">
                    <div class="col-md-12 text-center">
                        % if results.get('plot_time'):
                        <a href="/static/temp/{{ results['plot_time'] }}" download class="btn btn-default">💾 Скачать график динамики (PNG)</a>
                        % end
                        % if results.get('plot_phase'):
                        <a href="/static/temp/{{ results['plot_phase'] }}" download class="btn btn-default">💾 Скачать фазовый портрет (PNG)</a>
                        % end
                        % if results.get('csv_file'):
                        <a href="/static/temp/{{ results['csv_file'] }}" download class="btn btn-default">📥 Скачать данные (CSV)</a>
                        % end
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
% end