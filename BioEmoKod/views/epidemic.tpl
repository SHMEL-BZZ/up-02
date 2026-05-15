% rebase('layout.tpl', title=title, year=year)

<!-- Подключение уникальных стилей для страницы эпидемии -->
<link rel="stylesheet" type="text/css" href="/static/content/epidemic.css" />

<div class="page-header">
    <h2>Модель «Распространение эпидемии»</h2>
</div>

<!-- теоретический блок  -->
<div class="row">
    <div class="col-md-12">
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
                                <p style="font-size: 14px;">Модель описывает распространение инфекции в популяции крыс, обитающих на двумерной сетке n×n. Каждая клетка может содержать до 4 особей.</p>
                                <p style="font-size: 14px;">Состояния особей:</p>
                                <ul style="font-size: 14px;">
                                    <li><strong style="color: #2ecc71;">S (Susceptible)</strong> — здоровые, восприимчивые к заражению</li>
                                    <li><strong style="color: #e74c3c;">I (Infectious)</strong> — заражённые (инфекционные), болеют 6 дней</li>
                                    <li><strong style="color: #f1c40f;">R (Recovered)</strong> — невосприимчивые (иммунитет на 4 дня)</li>
                                </ul>
                                <p style="font-size: 14px;">Ключевые механизмы: перемещение в соседние клетки, заражение при контакте, циклический переход S→I→R→S, вакцинация.</p>
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
                                <p style="font-size: 14px;">Входные параметры модели:</p>
                                <ul style="font-size: 14px;">
                                    <li>n — размер сетки (n×n клеток)</li>
                                    <li>rats — общее количество особей</li>
                                    <li>p_infect — вероятность заражения при контакте</li>
                                    <li>p_move — вероятность перемещения в соседнюю клетку</li>
                                    <li>t — длительность симуляции (в неделях)</li>
                                    <li>day_vac — день, в который происходит вакцинация</li>
                                    <li>v — доля здоровых особей, получающих прививку</li>
                                </ul>
                                <p style="font-size: 14px;">Алгоритм одного дня: перемещение крыс внутри сетки → заражение здоровых крыс больными → получение объектами S/R статуса → вакцинация (в заданный день).</p>
                                <p style="font-size: 14px;">Фиксированные параметры: длительность болезни = 6 дней, иммунитет = 4 дня.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Пример работы приложения -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">
                                    🖥️ Пример работы приложения
                                </a>
                            </h4>
                        </div>
                        <div id="collapse3" class="panel-collapse collapse">
                            <div class="panel-body">
                                
                                <!-- ШАГ 1 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 1. Задание пространственных и временных параметров</h5>
                                    <p style="font-size: 14px;">В расчётной панели задайте:</p>
                                    <ul style="font-size: 14px;">
                                        <li>Размер сетки (n) — например, 8 для сетки размером 8×8 клеток</li>
                                        <li>Общее число крыс (rats) — например, 64 особи</li>
                                        <li>Длительность симуляции (t) — например, 52 недели (1 год)</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Поля ввода пространственных и временных параметров</span>
                                    </div>
                                </div>

                                <!-- ШАГ 2 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 2. Задание параметров заражения и перемещения</h5>
                                    <p style="font-size: 14px;">В расчётной панели задайте:</p>
                                    <ul style="font-size: 14px;">
                                        <li>Вероятность перемещения (p_move) — например, 0.5 (50% шанс переместиться в соседнюю клетку)</li>
                                        <li>Вероятность заражения (p_infect) — например, 0.6 (60% шанс заразиться при контакте с больным)</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Поля ввода вероятностей перемещения и заражения</span>
                                    </div>
                                </div>

                                <!-- ШАГ 3 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 3. Задание параметров вакцинации</h5>
                                    <p style="font-size: 14px;">В расчётной панели задайте:</p>
                                    <ul style="font-size: 14px;">
                                        <li>День начала вакцинации (day_vac) — например, 58-й день</li>
                                        <li>Процент вакцинируемых здоровых крыс (v) — например, 50%</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Поля настройки вакцинации</span>
                                    </div>
                                </div>

                                <!-- ШАГ 4 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 4. Запуск расчёта</h5>
                                    <p style="font-size: 14px;">Нажмите зелёную кнопку <strong>«Запустить расчёт»</strong> внизу расчётной панели.</p>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Кнопка запуска расчёта</span>
                                    </div>
                                </div>

                                <!-- ШАГ 5 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 5. Просмотр матрицы</h5>
                                    <p style="font-size: 14px;">После расчёта в блоке «Визуализация матрицы»:</p>
                                    <ul style="font-size: 14px;">
                                        <li>В каждой клетке отображается количество крыс каждого статуса (S, I, R)</li>
                                        <li>Цветовое кодирование: 🟢 S, 🔴 I, 🟡 R</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Визуализация матрицы n×n</span>
                                    </div>
                                </div>

                                <!-- ШАГ 6 -->
                                <div style="margin-bottom: 25px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 6. Анализ результатов</h5>
                                    <p style="font-size: 14px;">В блоке «Динамика эпидемии и анализ» представлены:</p>
                                    <ul style="font-size: 14px;">
                                        <li>График динамики SIR — изменение численности здоровых (S), заражённых (I) и иммунных (R) во времени</li>
                                        <li>Порог эпидемии — рассчитанный статистически уровень заболеваемости</li>
                                        <li>Эффективность вакцинации — в процентах (низкая &lt;50%, средняя 50-80%, высокая &gt;80%)</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] График динамики SIR и численные показатели</span>
                                    </div>
                                </div>

                                <!-- ШАГ 7 -->
                                <div style="margin-bottom: 10px;">
                                    <h5 style="font-size: 15px; font-weight: bold; color: #4E653D;">Шаг 7. Экспорт данных</h5>
                                    <p style="font-size: 14px;">Нажмите на соответствующие кнопки, чтобы сохранить результаты:</p>
                                    <ul style="font-size: 14px;">
                                        <li>CSV — численные данные динамики SIR</li>
                                        <li>PNG — график динамики</li>
                                    </ul>
                                    <div class="step-placeholder" style="background: #f5f5f5; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <span class="text-muted">[СКРИНШОТ] Кнопки экспорта данных</span>
                                    </div>
                                </div>

                                <!-- Итоговое резюме -->
                                <div class="alert alert-success" style="margin-top: 20px; font-size: 14px;">
                                    <strong>✅ Итог:</strong> После выполнения всех шагов вы получите полную картину распространения эпидемии, сможете оценить эффективность вакцинации и определить пороговые значения заболеваемости.
                                </div>
                            </div>
                        </div>
                    </div>

                </div> <!-- panel-group -->
            </div> <!-- panel-body -->
        </div> <!-- panel-info -->
    </div> <!-- col-md-12 -->
</div> <!-- row -->
