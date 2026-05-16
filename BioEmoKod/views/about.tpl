
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
                Разработка модуля "Модель хищник-жертва". Заполнение содержания главной страницы, создание файла README.
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
                Разработка модуля "Динамика рыбного промысла". Создание и настройка репозитория на gitgub, определение общей структуры проекта.
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
                Разработка модуля "Конкуренция видов". UX/UI дизайн, подбор цветовой схемы и шрифтов.
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
                Разработка модуля "Распространение эпидемии". UX/UI дизайн, подбор цветовой схемы и шрифтов.
            </p>
        </div>
    </div>

</div>