<p>
{{person.io_handler.get_output()}}
</p>
{% set cls_id = 1 %}
{%if person.__class__.__name__ == 'Leader'%}
    {% set cls_id = 2 %}
{% endif %}
<a href="{{selfurl}}/edit_form/{{cls_id}}/{{person.id}}">Edit</a>
<a href="{{selfurl}}/delete/{{person.id}}">Delete</a>
<br><br>