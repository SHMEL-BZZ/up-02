% rebase('layout.tpl', title=title, year=year, active_page='fishing')

<head>
    <link rel="stylesheet" type="text/css" href="/static/content/fishing.css" />
</head>

<div class="page-header">
    <h2>{{ title }}.</h2>
</div>

<!-- Аккордеон с раскрывающимися разделами -->
<div class="panel-group" id="fishing-accordion">

    <!-- Блок расчёта -->
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
                                            <input type="number" name="N" class="form-control" value="15" placeholder="N" required>
                                            <span class="help-block">10–100</span>
                                        </div>
                                        <div class="col-xs-6">
                                            <input type="number" name="M" class="form-control" value="15" placeholder="M" required>
                                            <span class="help-block">10–100</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Начальная численность (K):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="K" class="form-control" value="50" required>
                                    <span class="help-block">1–N*M</span>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h4 class="text-center">Вероятности процессов</h4>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Размножение (prepro):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="prepro" class="form-control" value="0.2" step="0.01" required>
                                    <span class="help-block">0.0 – 1.0</span>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-sm-6 control-label">Гибель (pdeath):</label>
                                <div class="col-sm-6">
                                    <input type="number" name="pdeath" class="form-control" value="0.1" step="0.01" required>
                                    <span class="help-block">0.0 – 1.0</span>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="form-group">
                            <div class="col-sm-offset-4 col-sm-4">
                                <button type="submit" class="btn btn-fishing btn-block">Найти оптимальный q</button>
                            </div>
                        </div>
                    </div>

                    % if defined('error') and error:
                    <div class="alert alert-danger">
                        <strong>Ошибка:</strong> {{ error }}
                    </div>
                    % end
                </form>

                % if graph_base64:
                <div class="well">
                    <h4 class="text-center">Результаты оптимизации</h4>
                    <p><strong>Оптимальная вероятность вылова (q_opt):</strong> {{ results['q_opt'] }}</p>
                    <p><strong>Средний улов при q_opt:</strong> {{ results['avg_catch_opt'] }}</p>
                    <p><strong>Средняя численность при q_opt:</strong> {{ results['avg_pop_opt'] }}</p>

                    <div class="chart-title">График зависимости:</div>
                    <img src="data:image/png;base64,{{ graph_base64 }}" class="img-responsive" style="width:100%; max-width:800px; margin:0 auto;">

                    <div class="text-center" style="margin: 20px 0;">
                        <button id="downloadPngBtn" class="btn btn-save-accent">Скачать график (PNG)</button>
                        <button id="downloadCsvBtn" class="btn btn-save-accent">Скачать данные (CSV)</button>
                    </div>
                </div>
                % end

                % if frames_by_q and q_animation_list_json and N and M:
                <div class="well">
                    <h4 class="text-center">Анимация модели для всех q (от 0.0 до 1.0)</h4>
                    <div class="grid-container">
                        <table class="grid-table" id="animation-grid">
                            % for i in range(N):
                            <tr>
                                % for j in range(M):
                                <td id="cell-{{ i }}-{{ j }}" class="empty-cell"></td>
                                % end
                            </tr>
                            % end
                        </table>
                    </div>
                    <div class="text-center">
                        <p>Текущее значение q: <strong><span id="currentQ">0.00</span></strong></p>
                        <button id="startSeriesBtn" class="btn btn-fishing">▶ Старт серии</button>
                        <button id="pauseSeriesBtn" class="btn btn-fishing">⏸ Пауза</button>
                        <button id="resetSeriesBtn" class="btn btn-fishing">⟳ Сброс</button>
                        <div style="margin-top: 10px;">
                            <label>Скорость анимации (мс):
                                <input type="range" id="seriesSpeedSlider" min="50" max="500" value="200" step="10">
                                <span id="speedValue">200</span>
                            </label>
                        </div>
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

<script>
// Данные от сервера 
var qList = {{! q_animation_list_json }};
var framesByQ = {{! frames_by_q_json }};
var N = {{ N if N else 0 }};
var M = {{ M if M else 0 }};

// Состояние анимации
var currentQIndex = 0;
var currentFrameIndex = 0;
var intervalId = null;
var speed = 200;
var framesForCurrentQ = [];

// Обновление отображения сетки
function renderCurrentFrame() {
    if (!framesForCurrentQ || framesForCurrentQ.length === 0) return;
    var frame = framesForCurrentQ[currentFrameIndex];
    for (var i = 0; i < N; i++) {
        for (var j = 0; j < M; j++) {
            var cell = document.getElementById('cell-' + i + '-' + j);
            if (!cell) continue;
            var hasFish = frame[i][j] === 1;
            if (hasFish) {
                cell.className = 'fish-cell';
                cell.innerHTML = '<span class="fish-icon">&bull;</span>';
            } else {
                cell.className = 'empty-cell';
                cell.innerHTML = '';
            }
        }
    }
}

// Загрузить анимацию для q с индексом index
function loadQ(index) {
    if (index >= qList.length) {
        stopSeries();
        alert("Анимация завершена для всех значений q");
        return false;
    }
    var qVal = qList[index];
    document.getElementById('currentQ').innerText = qVal;
    //  Число в строку 
    var key = qVal.toFixed(2);
    framesForCurrentQ = framesByQ[key];
    currentFrameIndex = 0;
    if (framesForCurrentQ && framesForCurrentQ.length) {
        renderCurrentFrame();
        updateProgress();
        return true;
    }
    return false;
}

// Один шаг анимации 
function stepAnimation() {
    if (!framesForCurrentQ) return;
    if (currentFrameIndex + 1 < framesForCurrentQ.length) {
        currentFrameIndex++;
        renderCurrentFrame();
        updateProgress();
    } else {
        // переход к следующему q
        currentQIndex++;
        if (!loadQ(currentQIndex)) {
            stopSeries();
        } else {
            updateProgress();
        }
    }
}

function startSeries() {
    if (intervalId) clearInterval(intervalId);
    if (currentQIndex === 0 && currentFrameIndex === 0) {
        if (!loadQ(0)) return;
    }
    intervalId = setInterval(stepAnimation, speed);
}

function stopSeries() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

function resetSeries() {
    stopSeries();
    currentQIndex = 0;
    loadQ(0);
}

function updateProgress() {
    if (!framesForCurrentQ || framesForCurrentQ.length === 0) return;
    var totalFramesForCurrent = framesForCurrentQ.length;
    var currentFrame = currentFrameIndex;
    var totalQ = qList.length;
    var completedFrames = currentQIndex * totalFramesForCurrent + currentFrame;
    var totalFramesAll = totalQ * totalFramesForCurrent;
    var percent = Math.floor((completedFrames / totalFramesAll) * 100);
    var progressBar = document.getElementById('animationProgress');
    if (progressBar) {
        progressBar.style.width = percent + '%';
        progressBar.innerText = percent + '%';
    }
}

// Обработчики кнопок
document.getElementById('startSeriesBtn').addEventListener('click', startSeries);
document.getElementById('pauseSeriesBtn').addEventListener('click', stopSeries);
document.getElementById('resetSeriesBtn').addEventListener('click', resetSeries);

// Кнопка сохранения PNG
document.getElementById('downloadPngBtn').addEventListener('click', function() {
    const imgSrc = document.querySelector('img[src^="data:image/png;base64,"]')?.src;
    if (imgSrc) {
        const link = document.createElement('a');
        link.href = imgSrc;
        link.download = 'graph.png';
        link.click();
    } else {
        alert('График ещё не сгенерирован');
    }
});

// Кнопка сохранения CSV
document.getElementById('downloadCsvBtn').addEventListener('click', function() {
    const tableData = {{! table_data_json }};
    if (!tableData.length) {
        alert('Нет данных для сохранения');
        return;
    }
    let csvContent = "q,avg_catch,avg_pop\n";
    tableData.forEach(row => {
        csvContent += `${row.q},${row.avg_catch},${row.avg_pop}\n`;
    });
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'fishing_results.csv';
    link.click();
    URL.revokeObjectURL(link.href);
});

var speedSlider = document.getElementById('seriesSpeedSlider');
if (speedSlider) {
    speedSlider.addEventListener('input', function(e) {
        speed = parseInt(e.target.value);
        document.getElementById('speedValue').innerText = speed;
        if (intervalId) {
            stopSeries();
            startSeries();
        }
    });
}

if (qList.length && framesByQ) {
    loadQ(0);
}
</script>