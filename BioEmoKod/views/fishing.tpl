% rebase('layout.tpl', title=title, year=year, active_page='fishing')

<head>
    <link rel="stylesheet" type="text/css" href="/static/content/fishing.css" />
</head>

<div class="page-header">
    <h2>{{ title }}.</h2>
</div>

<!-- Аккордеон с раскрывающимися разделами -->
<div class="panel-group" id="fishing-accordion">

    <!-- Раздел программа  -->
    <div class="panel panel-primary">
        <div class="panel-heading">
            <h3 class="panel-title">
                <a data-toggle="collapse" data-parent="#fishing-accordion" href="#collapseProgram">
                    Поиск оптимального вылова
                </a>
            </h3>
        </div>
        <div id="collapseProgram" class="panel-collapse collapse in">
            <div class="panel-body">
                <form method="post" action="/fishing">
                    <div class="row">
                        <div class="col-md-6">
                            <h4 class="text-center">Параметры сетки и популяции</h4>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Размер сетки (N x M):</label>
                                <div class="col-sm-6">
                                    <div class="row">
                                        <div class="col-xs-6">
                                            <input type="number" name="N" class="form-control" value="15" placeholder="N">
                                            <span class="help-block">10–200</span>
                                        </div>
                                        <div class="col-xs-6">
                                            <input type="number" name="M" class="form-control" value="15" placeholder="M">
                                            <span class="help-block">10–200</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Начальная численность (K):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="K" class="form-control" value="50" required>
                                    <span class="help-block">10–200</span>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h4 class="text-center">Вероятности процессов</h4>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Размножение (p_repro):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="p_repro" class="form-control" value="0.25" step="0.01" required>
                                    <span class="help-block">от 0 до 1</span>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Гибель (p_death):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="p_death" class="form-control" value="0.1" step="0.01" required>
                                    <span class="help-block">от 0 до 1</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr>
                    <div class="form-group">
                        <div class="col-sm-offset-4 col-sm-4">
                            <button type="submit" class="btn btn-fishing btn-block">Найти оптимальный q</button>
                        </div>
                    </div>
                </form>

                <!-- Блок результатов -->
                % if defined('grid') and grid:
                <div class="well">
                    % if defined('q'):
                    <p class="text-center">
                        <strong>Текущий q: {{ q }}</strong>
                    </p>
                    % end

                    <div class="grid-container">
                        <table class="grid-table">
                            % for row in grid:
                            <tr>
                                % for cell in row:
                                <td class="{{'fish-cell' if cell else 'empty-cell'}}">
                                    % if cell:
                                    <span class="fish-icon">&bull;</span>
                                    % end
                                </td>
                                % end
                            </tr>
                            % end
                        </table>
                    </div>

                    <div class="col-sm-6 chart-title">
                        <label>Средняя популяция в зависимости от q:</label>
                    </div>
                    <!-- График-заглушка -->
                    <div class="chart-placeholder">
                        График зависимости среднего значения популяции от вылова
                    </div>

                    <div class="text-center" style="margin-top: 20px;">
                        <button type="button" class="btn btn-save-accent btn-block">
                            Сохранить результаты симуляции
                        </button>
                    </div>
                </div>
                % end
            </div>
        </div>
    </div>

    <!-- Теория -->
    <div class="panel panel-info">
        <div class="panel-heading">
            <h3 class="panel-title">
                <a data-toggle="collapse" data-parent="#fishing-accordion" href="#collapseTheory">
                    Теория
                </a>
            </h3>
        </div>
        <div id="collapseTheory" class="panel-collapse collapse">
            <div class="panel-body">
                <div class="theory-content">
                    <p><strong>Модель популяции рыб</strong> работает на двумерной прямоугольной сетке N × M, где каждая клетка либо содержит рыбу (True), либо пуста (False). Один шаг симуляции включает четыре последовательные фазы.</p>
                    <p>Сначала создается список значений <strong>q</strong> (вероятности вылова). Алгоритм для каждого значения q:</p>
                    <p>Для каждого повторения <strong>trials</strong> (число прогонов, для дальнейшего получения среднего значения). Половина шагов не учитываются в статистике для стабилизации системы, для остальной половины высчитывается суммарное количество популяции и вылова.</p>
                    <p><strong>1. Инициализация</strong><br>
                    - Создаётся сетка N × M, заполненная пустыми клетками.<br>
                    - Случайным образом (без повторений) выбирается K клеток, в каждую из них помещается по одной рыбе.</p>
                    <p><strong>Один шаг (step):</strong></p>
                    <p><strong>2. Движение:</strong> все рыбы обрабатываются в случайном порядке (чтобы избежать систематических конфликтов). Каждая рыба выбирает одну из 9 возможных позиций: 8 соседей (включая диагональные) или свою текущую клетку. Если выбранная клетка свободна и отличается от текущей, рыба перемещается туда; иначе остаётся на месте. Перемещённая рыба не влияет на перемещение других в том же шаге.</p>
                    <p><strong>3. Размножение:</strong> все рыбы (уже после движения) перебираются в случайном порядке. Для каждой рыбы с вероятностью <strong>prepro</strong> происходит попытка размножения: из всех свободных соседних клеток (без учёта текущей) случайно выбирается одна для потомка. Список отобранных клеток собирается, затем потомки добавляются (если клетка всё ещё свободна). Если несколько рыб выбрали одну клетку – туда попадёт только один потомок (за счёт преобразования списка в множество).</p>
                    <p><strong>4. Естественная смертность:</strong> каждая рыба независимо с вероятностью <strong>p_death</strong> погибает (клетка становится пустой).</p>
                    <p><strong>5. Промысловый вылов:</strong><br>
                    - Каждая оставшаяся рыба независимо с вероятностью <strong>q</strong> вылавливается (клетка обнуляется). Подсчитывается количество выловленных рыб за этот шаг.<br>
                    - Высчитывается общее значение вылова и популяции за все шаги.<br>
                    - Номер шага увеличивается на единицу.</p>
                    <p>Все прогоны усредняются – получаем среднее значение вылова (<strong>avg_catch</strong>) и среднее значение популяции (<strong>avg_pop</strong>) для текущего q.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Пример -->
    <div class="panel panel-success">
        <div class="panel-heading">
            <h3 class="panel-title">
                <a data-toggle="collapse" data-parent="#fishing-accordion" href="#collapseExample">
                    Пример работы модели
                </a>
            </h3>
        </div>
        <div id="collapseExample" class="panel-collapse collapse">
            <div class="panel-body">
                <div class="chart-title">
                    <h4>Пример входных данных:</h4>
                    <img src="/static/img/primer.png" alt="График зависимости средней популяции от q" style="max-width: 100%; height: auto;">
                    <h4>Пример графика зависимости средней популяции от q:</h4>
                    <!-- График-заглушка -->
                    <div class="chart-placeholder">
                        График зависимости среднего значения популяции от вылова
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>