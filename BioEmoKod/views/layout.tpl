<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - BioEmoCode</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <a class="navbar-brand" href="/home" style="color: white !important; text-decoration: none !important; font-size: 28px; font-weight: bold; margin-right: 50px;">BioEmoCode</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="{{ 'active' if active_page == 'home' else '' }}">
                        <a href="/home" style="color: white !important;">Главная</a>
                    </li>
                    <li class="{{ 'active' if active_page == 'predator_pray' else '' }}">
                        <a href="/predator_pray" style="color: white !important;">Хищник-жертва</a>
                    </li>
                    <li class="{{ 'active' if active_page == 'epidemic' else '' }}">
                        <a href="/epidemic" style="color: white !important;">Эпидемия</a>
                    </li>
                    <li class="{{ 'active' if active_page == 'competition' else '' }}">
                        <a href="/competition" style="color: white !important;">Конкуренция</a>
                    </li>
                    <li class="{{ 'active' if active_page == 'fishing' else '' }}">
                        <a href="/fishing" style="color: white !important;">Рыболовство</a>
                    </li>
                    <li class="{{ 'active' if active_page == 'about' else '' }}">
                        <a href="/about" style="color: white !important;">Об авторах</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - BioEmoCode</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>