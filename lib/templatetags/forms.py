from django.template import Library
from django import forms


register = Library()

@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)

@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)

@register.filter
def is_check(field):
    return isinstance(field.field.widget, (forms.CheckboxInput, forms.RadioSelect))

@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)

@register.filter
def bootstrap_class(field):
    field_classes = set(field.field.widget.attrs.get('class', '').split())

    if is_check(field):
        field_classes.add('form-check-input')
    elif is_select(field):
        field_classes.add('form-select')
    else:
        field_classes.add('form-control')

    if field.form.is_bound:
        if field.errors:
            field_classes.add('is-invalid')
        else:
            field_classes.add('is-valid')

    field.field.widget.attrs['class'] = ' '.join(field_classes)
    return field
