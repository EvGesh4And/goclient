<html>
<head><title>Lab 4</title></head>
<body>
<h3>Lab 4:</h3>

{% for title, bp in bps %}
    <a href="st{{loop.index}}">{{title}}</a><br>
{% endfor %}

</body></html>
