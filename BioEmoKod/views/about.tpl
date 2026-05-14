
% rebase('layout.tpl', title=title, year=year)

<!-- специальный стиль для страницы Авторы -->
<head>
    <link rel="stylesheet" type="text/css" href="/static/content/about.css" />
</head>

<div class="page-header">
    <h2>{{ title }}</h2>
</div>
<div class="authors-list">

    <!-- Рита -->
    <div class="author-row">
        <img src="/static/img/rita.jpg" alt="Рита" class="author-photo">
        <div class="author-info">
            <div class="author-name">Скулябина Маргарита</div>
            <div class="author-divider"></div>
            <p class="author-contribution">
                Разработка клиентской части (frontend). Вёрстка интерфейса, анимации, интеграция с API.
            </p>
        </div>
    </div>

    <!-- Катя -->
    <div class="author-row">
        <img src="/static/img/kate.jpg" alt="Катя" class="author-photo">
        <div class="author-info">
            <div class="author-name">Андреева Екатерина</div>
            <div class="author-divider"></div>
            <p class="author-contribution">
                Серверная логика и базы данных. Проектирование REST API, безопасность, оптимизация запросов.
            </p>
        </div>
    </div>

    <!-- Ника -->
    <div class="author-row">
        <img src="/static/img/nika.jpg" alt="Ника" class="author-photo">
        <div class="author-info">
            <div class="author-name">Волкова Ника</div>
            <div class="author-divider"></div>
            <p class="author-contribution">
                UX/UI дизайн и прототипирование. Разработка макетов в Figma, подбор цветовой схемы и шрифтов.
            </p>
        </div>
    </div>

    <!-- Оля -->
    <div class="author-row">
        <img src="/static/img/ola.jpg" alt="Оля" class="author-photo">
        <div class="author-info">
            <div class="author-name">Пароменкова Ольга</div>
            <div class="author-divider"></div>
            <p class="author-contribution">
                Тестирование и документация. Написание автотестов, руководства пользователя, баг-трекинг.
            </p>
        </div>
    </div>

</div>