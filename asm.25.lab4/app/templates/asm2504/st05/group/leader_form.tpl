{% extends "asm2504/st05/group/base.tpl" %}

{% block content %}

{% if person.id != 0%}
    <form action = '{{selfurl}}/edit' method=Post>
{% else %}
    <form action = '{{selfurl}}/add' method=POST>
{% endif %}

<input type="hidden" name=obj_class value="2">

<input type=hidden name=id value={{person.id}}>
Имя:<input type=text name=name value={{person.name}}><br>
Возраст:<input type=text name=age value={{person.age}}>
Группа: <input type=text name=group value={{person.group}}>
<br><input type=submit value="Ok">
</form>

{% endblock %}