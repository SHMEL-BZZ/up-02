% rebase('layout.tpl', title='Главная', year=year)

<div class="page-header">
    <div class="header-container">
        <div class="header-image">
            <img src="/static/img/logo.jpg" alt="BioEmoCode Logo" class="rounded-logo">
        </div>
        <div class="header-text">
            <h1>БиоЭмоКод</h1>
            <p class="lead">Биологический экспериментальный модульный образец</p>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-12">
        <div class="well" style="padding: 20px;">
            <h3 style="font-size: 18px; font-weight: bold; color: #4E653D;">О проекте</h3>
            <p style="font-size: 14px; line-height: 1.5;">
                <strong>«БиоЭмоКод»</strong> — это веб-приложение для численного моделирования и визуализации динамики 
                биологических и экологических систем. Комплекс предназначен для исследования нелинейной динамики экосистем, 
                визуализации бифуркаций и анализа устойчивости популяций.
            </p>
            <p style="font-size: 14px; line-height: 1.5;">
                Приложение разработано в рамках учебной практики по интеграции программных модулей и позволяет 
                перейти от статического изучения уравнений к интерактивному анализу экосистем.
            </p>
        </div>

        <h3 style="font-size: 18px; font-weight: bold; color: #4E653D;">Математические модели</h3>
        
        <!-- Первая строка блоков -->
        <div class="row row-flex">
            <div class="col-md-6">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 style="font-size: 16px;">📊 Хищник-жертва</h4>
                    </div>
                    <div class="panel-body" style="font-size: 14px;">
                        <p>Классическая модель Лотки-Вольтерры взаимодействия двух видов:</p>
                        <ul style="padding-left: 20px;">
                            <li><strong>Кролики (жертвы)</strong> — размножаются, погибают при встречах с хищниками</li>
                            <li><strong>Лисы (хищники)</strong> — размножаются за счёт съеденных жертв, гибнут от голода</li>
                        </ul>
                        <p><em>Параметры: скорость размножения, эффективность охоты, смертность хищников</em></p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 style="font-size: 16px;">🦠 Распространение эпидемии</h4>
                    </div>
                    <div class="panel-body" style="font-size: 14px;">
                        <p>SIR-модель распространения инфекционного заболевания:</p>
                        <ul style="padding-left: 20px;">
                            <li><strong>S</strong> — восприимчивые к заболеванию</li>
                            <li><strong>I</strong> — инфицированные</li>
                            <li><strong>R</strong> — выздоровевшие с иммунитетом</li>
                        </ul>
                        <p><em>Позволяет определить порог эпидемии и оценить эффективность вакцинации</em></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Вторая строка блоков -->
        <div class="row row-flex">
            <div class="col-md-6">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 style="font-size: 16px;">⚔️ Конкуренция видов</h4>
                    </div>
                    <div class="panel-body" style="font-size: 14px;">
                        <p>Модель конкуренции двух видов за общий пищевой ресурс.</p>
                        <ul style="padding-left: 20px;">
                            <li>Исследование условий сосуществования видов</li>
                            <li>Анализ конкурентного исключения</li>
                            <li>Определение устойчивого равновесия</li>
                        </ul>
                        <p><em>Позволяет определить, какой вид вытеснит другой или возможна ли стабильная конкуренция</em></p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 style="font-size: 16px;">🎣 Динамика рыбного промысла</h4>
                    </div>
                    <div class="panel-body" style="font-size: 14px;">
                        <p>Модель Шефера — популяция рыбы с учётом промыслового вылова.</p>
                        <ul style="padding-left: 20px;">
                            <li>Оценка порогов устойчивости эксплуатируемых популяций</li>
                            <li>Поиск оптимального уровня вылова</li>
                            <li>Устойчивое развитие рыбопромысловых хозяйств</li>
                        </ul>
                        <p><em>Позволяет найти баланс между выловом и сохранением популяции</em></p>
                    </div>
                </div>
            </div>
        </div>

        <div class="alert alert-info" style="font-size: 14px;">
            <strong>📌 Для работы с приложением:</strong> используйте верхнее меню для выбора интересующей модели. 
            На каждой странице вы сможете задать параметры моделирования, запустить расчёт и получить графики динамики популяций.
        </div>
    </div>
</div>