% rebase('layout.tpl', title=title, year=year)

<!-- специальный стиль для страницы Модель хищник-жертва -->
<head>
    <link rel="stylesheet" type="text/css" href="/static/content/predator_pray.css" />
</head>

<div class="page-header">
    <h2>Модель «Хищник-жертва»</h2>
</div>

<!-- Верхняя строка: теория + картинки в колонке -->
<div class="row">
    <div class="col-md-8">
        <!-- БЛОК ТЕОРИИ (аккордеон) -->
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">Теоретические сведения</h3>
            </div>
            <div class="panel-body">
                <div class="panel-group" id="accordion">

                    <!-- 1. Модель Лотки–Вольтерры -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
                                    Модель «Хищник-жертва» (Лотки-Вольтерры)
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
                                    Система дифференциальных уравнений
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
                                    Равновесие и анализ устойчивости
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
                                    Примеры сценариев
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

                    <!-- 5. Источники -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse5">
                                    Источники
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

                </div> <!-- panel-group -->
            </div> <!-- panel-body -->
        </div> <!-- panel-info -->
    </div> <!-- col-md-8 -->

    <!-- Картинки в колонке справа -->
    <div class="col-md-4">
        <div class="panel panel-default">
            <div class="panel-body text-center">

                <!-- Картинка жертвы -->
                <div class="row">
                    <div class="col-xs-12">
                        <img src="/static/img/bunny.jpg"
                             class="img-responsive"
                             style="height: 250px; width: 100%; object-fit: cover;"
                             alt="Заяц">
                        <p class="text-muted" style="margin-top: 10px;">Жертва (заяц)</p>
                    </div>
                </div>

                <!-- Картинка хищника -->
                <div class="row">
                    <div class="col-xs-12">
                        <img src="/static/img/fox.jpg"
                             class="img-responsive"
                             style="height: 250px; width: 100%; object-fit: cover;"
                             alt="Лиса">
                        <p class="text-muted" style="margin-top: 10px;">Хищник (лиса)</p>
                    </div>
                </div>

            </div> <!-- panel-body -->
        </div> <!-- panel-default -->
    </div> <!-- col-md-4 -->
</div> <!-- row -->

<!-- Расчётная панель -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title text-center">Расчётная панель</h3>
            </div>
            <div class="panel-body">

                <form action="/predator_pray" method="post" class="form-horizontal">

                    <!-- Два столбца -->
                    <div class="row">

                        <!-- ЛЕВАЯ КОЛОНКА: Начальные условия + симуляция -->
                        <div class="col-md-6">

                            <h4 class="text-center">Начальные условия</h4>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Число жертв x₀:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="any" name="x0" class="form-control" value="50" required>
                                            <span class="help-block">Диапазон: 10–100</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Число хищников y₀:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="any" name="y0" class="form-control" value="20" required>
                                            <span class="help-block">Диапазон: 1–50</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <hr>

                            <h4 class="text-center">Параметры симуляции</h4>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Длительность T (лет):</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="1" name="T" class="form-control" value="50" required>
                                            <span class="help-block">Диапазон: 5–50</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Число шагов N:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="100" name="N" class="form-control" value="1000" required>
                                            <span class="help-block">Диапазон: 200–10000</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- col-md-6 (левая колонка) -->

                        <!-- ПРАВАЯ КОЛОНКА: Параметры модели -->
                        <div class="col-md-6">

                            <h4 class="text-center">Параметры модели</h4>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Рождаемость жертв α:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="0.01" name="alpha" class="form-control" value="0.8" required>
                                            <span class="help-block">Диапазон: 0.4–1.5</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Эффективность охоты c:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="0.01" name="c" class="form-control" value="0.04" required>
                                            <span class="help-block">Диапазон: 0.01–0.06</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Смертность хищников β:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="0.01" name="beta" class="form-control" value="0.6" required>
                                            <span class="help-block">Диапазон: 0.4–1.5</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label class="col-sm-6 control-label">Рост хищников d:</label>
                                        <div class="col-sm-6">
                                            <input type="number" step="0.01" name="d" class="form-control" value="0.02" required>
                                            <span class="help-block">Диапазон: 0.01–0.06</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- col-md-6 (правая колонка) -->

                    </div> <!-- row (два столбца) -->

                    <hr>

                    <!-- Кнопка запуска -->
                    <div class="form-group">
                        <div class="col-sm-offset-5 col-sm-2">
                            <button type="submit" class="btn btn-success btn-block">Запустить расчёт</button>
                        </div>
                    </div>

                </form>
            </div> <!-- panel-body -->
        </div> <!-- panel-primary -->
    </div> <!-- col-md-12 -->
</div> <!-- row -->

<!-- Отображение ошибок -->
% if defined('error') and error:
<div class="row">
    <div class="col-md-12">
        <div class="alert alert-danger">
            <strong>Ошибка:</strong> {{ error }}
            <button type="button" class="close" data-dismiss="alert">&times;</button>
        </div>
    </div>
</div>
% end

<!-- Результаты расчёта (если есть) -->
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
                             class="img-responsive img-thumbnail" 
                             style="width: 100%;"
                             alt="Графики динамики и фазовый портрет">
                    </div>
                </div>

                <hr>

                <div class="row">
                    <div class="col-md-12">
                        <h4 class="text-center">Анализ результатов</h4>
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
                
            </div> <!-- panel-body -->
        </div> <!-- panel-success -->
    </div> <!-- col-md-12 -->
</div> <!-- row -->
% end