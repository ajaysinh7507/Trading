from operator import index
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def split(value, split_by):
    return value.split(split_by)

@register.filter
def indexOf(value, index_of):
    return value[index_of]

@register.filter
def dateFormat(date, formats):
    formats = eval(formats)
    # print(eval('10+10'))
    datetime_object = datetime.strptime(date, formats['currentFormat'])
    return datetime_object.strftime(formats['requiredFormat'])