{% extends "asm2504/st05/group/base.tpl" %}

{% include "asm2504/st05/group/load_from_pickle.tpl" ignore missing %}

{% block content %}
    {% for person in group %}
{% include "asm2504/st05/group/item.tpl" ignore missing %}
    {% else %}
Group is empty
    {% endfor %}

{% include "asm2504/st05/group/add_student.tpl" ignore missing %}
{% include "asm2504/st05/group/add_leader.tpl" ignore missing %}

{% endblock %}