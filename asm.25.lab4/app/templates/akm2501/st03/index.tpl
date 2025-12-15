<!DOCTYPE html>
<html>
<head>
    <title>Лабораторная работа 4</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Лабораторная работа 4 - REST API</h1>
    <p>Выберите модуль для работы:</p>
    
    <ul>
        {% for title, bp in bps %}
        <li><a href="{{ url_for(bp.name + '.index') }}">{{ title }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>