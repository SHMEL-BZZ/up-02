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
                                <!-- Блок 1: Эпидемический порог -->
                                <div style="margin-bottom: 30px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
                                    <h5 style="font-size: 16px; font-weight: bold; color: #4E653D; margin-bottom: 15px;">📊 Расчёт эпидемического порога</h5>
                                    
                                    <p style="font-size: 14px;"><strong>Эпидемический порог</strong> — это критический уровень заболеваемости, при превышении которого эпидемия переходит в неуправляемую фазу. Расчёт производится на основе первых 8 недель симуляции (базовый период).</p>
                                    
                                    <p style="font-size: 14px; margin-top: 15px;"><strong>Шаг 1. Вычисление среднего арифметического заболеваемости за базовый период</strong></p>
                                    <div style="background: white; padding: 12px; border-left: 4px solid #4E653D; margin: 10px 0;">
                                        <p style="font-size: 16px; text-align: center; margin: 0;">
                                            X̄<sub>баз</sub> = (X₁ + X₂ + ... + Xₙ) / n
                                        </p>
                                    </div>
                                    <p style="font-size: 13px; color: #666;">где:</p>
                                    <ul style="font-size: 13px; color: #666;">
                                        <li>X̄<sub>баз</sub> — среднее арифметическое заболеваемости за базовый период</li>
                                        <li>Xᵢ — количество заражённых за i-ю неделю</li>
                                        <li>n — количество недель в базовом периоде (n = 8)</li>
                                    </ul>

                                    <p style="font-size: 14px; margin-top: 15px;"><strong>Шаг 2. Вычисление стандартного отклонения</strong></p>
                                    <div style="background: white; padding: 12px; border-left: 4px solid #4E653D; margin: 10px 0;">
                                        <p style="font-size: 16px; text-align: center; margin: 0;">
                                            σ<sub>баз</sub> = √[ Σ(Xᵢ - X̄<sub>баз</sub>)² / (n - 1) ]
                                        </p>
                                    </div>
                                    <p style="font-size: 13px; color: #666;">где σ<sub>баз</sub> — стандартное (среднеквадратичное) отклонение заболеваемости.</p>

                                    <p style="font-size: 14px; margin-top: 15px;"><strong>Шаг 3. Расчёт порога эпидемии</strong></p>
                                    <div style="background: white; padding: 12px; border-left: 4px solid #e74c3c; margin: 10px 0;">
                                        <p style="font-size: 16px; text-align: center; margin: 0;">
                                            X<sub>порог</sub> = X̄<sub>баз</sub> + 2,507 × σ<sub>баз</sub>
                                        </p>
                                    </div>
                                    <p style="font-size: 13px; color: #666;">где 2,507 — произведение коэффициента Стьюдента (2,365) и статистической поправки (√(1 + 1/n) ≈ 1,06066).</p>
                                </div>

                                <!-- Блок 2: Эффективность вакцинации -->
                                <div style="margin-bottom: 20px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
                                    <h5 style="font-size: 16px; font-weight: bold; color: #4E653D; margin-bottom: 15px;">💉 Расчёт эффективности вакцинации</h5>
                                    
                                    <p style="font-size: 14px;">Эффективность вакцинации оценивается путём сравнения двух сценариев развития эпидемии:</p>
                                    <ul style="font-size: 14px;">
                                        <li>Сценарий А — симуляция без вакцинации на всём временном интервале</li>
                                        <li>Сценарий Б — симуляция с вакцинацией (начиная с заданного пользователем дня)</li>
                                    </ul>

                                    <p style="font-size: 14px; margin-top: 15px;"><strong>Формула расчёта эффективности:</strong></p>
                                    <div style="background: white; padding: 12px; border-left: 4px solid #5cb85c; margin: 10px 0;">
                                        <p style="font-size: 16px; text-align: center; margin: 0;">
                                            Эффективность = (W<sub>без</sub> - W<sub>с</sub>) / W<sub>без</sub> × 100%
                                        </p>
                                    </div>
                                    <p style="font-size: 13px; color: #666;">где:</p>
                                    <ul style="font-size: 13px; color: #666;">
                                        <li><W<sub>без</sub> — количество эпидемических недель в сценарии без вакцинации</li>
                                        <li>W<sub>с</sub> — количество эпидемических недель в сценарии с вакцинацией</li>
                                    </ul>

                                    <p style="font-size: 14px; margin-top: 15px;"><strong>Критерии оценки эффективности:</strong></p>
                                    <div class="row" style="margin-top: 10px;">
                                        <div class="col-md-4 text-center">
                                            <div style="background: #d9534f; color: white; padding: 8px; border-radius: 8px;">
                                                <strong>Низкая</strong><br>
                                                &lt; 50%
                                            </div>
                                        </div>
                                        <div class="col-md-4 text-center">
                                            <div style="background: #f0ad4e; color: white; padding: 8px; border-radius: 8px;">
                                                <strong>Средняя</strong><br>
                                                50% – 80%
                                            </div>
                                        </div>
                                        <div class="col-md-4 text-center">
                                            <div style="background: #5cb85c; color: white; padding: 8px; border-radius: 8px;">
                                                <strong>Высокая</strong><br>
                                                &gt; 80%
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
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
</div>

<!-- блок: расчётная панель -->
<div class="row">
    <div class="col-md-12">
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title text-center">🧮 Расчётная панель</h3>
            </div>
            <div class="panel-body">
                <form action="/epidemic" method="post" class="form-horizontal">
                    
                    <div class="row">
                        <!-- колонка 1: Пространство и время -->
                        <div class="col-md-4">
                            <h5 style="font-size: 16px; font-weight: bold; margin-top: 0; margin-bottom: 15px; color: #4E653D;">Пространство и время</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Размер сетки n×n:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="grid_size" class="form-control" value="8" min="2" max="10" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">n = 2..10</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Общее число крыс:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="total_rats" class="form-control" value="64" min="1" max="400" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">максимум n²·4</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Длительность (недели):</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="weeks" class="form-control" value="52" min="8" max="260" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">8..260</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 2: Заражение и перемещение -->
                        <div class="col-md-4">
                            <h5 style="font-size: 16px; font-weight: bold; margin-top: 0; margin-bottom: 15px; color: #4E653D;">Заражение и перемещение</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Вероятность заражения:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.05" name="p_infect" class="form-control" value="0.6" min="0.1" max="0.9" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">0.1..0.9</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Вероятность перемещения:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="0.05" name="p_move" class="form-control" value="0.5" min="0.1" max="0.9" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">0.1..0.9</span>
                                </div>
                            </div>
                        </div>

                        <!-- колонка 3: Вакцинация -->
                        <div class="col-md-4">
                            <h5 style="font-size: 16px; font-weight: bold; margin-top: 0; margin-bottom: 15px; color: #4E653D;">Вакцинация</h5>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">День начала вакцинации:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="1" name="vacc_day" class="form-control" value="30" min="9" max="364" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">9..t·7 (максимум зависит от недель)</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="col-sm-12 control-label" style="font-size: 14px; text-align: left;">Процент вакцинируемых крыс:</label>
                                <div class="col-sm-12">
                                    <input type="number" step="5" name="vacc_percent" class="form-control" value="50" min="1" max="100" required style="font-size: 14px;">
                                    <span class="help-block" style="font-size: 11px;">1%..100%</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- кнопка запуска -->
                    <div class="form-group">
                        <div class="col-sm-12">
                            <button type="submit" class="btn" style="background-color: #468847; border-color: #4E653D; color: white; font-size: 14px; padding: 8px 24px; border-radius: 8px;">
                                ▶ Запустить расчёт
                            </button>
                        </div>
                    </div>

                </form>
            </div>
        </div>
    </div>
</div>