from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('categories.html')
def categories():
   categories_list = Category.objects.all()
   return {
      'categories': categories_list
      }

@register.inclusion_tag('categories_table.html')
def categories_table():
    categories_list = Category.objects.all()
    return {
        'categories': categories_list
    }