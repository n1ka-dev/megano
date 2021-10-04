from django import template
from django.db.models import Sum, F
from django.utils.safestring import mark_safe

from app_shop.models import Category

register = template.Library()


@register.simple_tag(takes_context=True)
def get_catalog_menu(context, *args, **kwargs):
    categories = Category.objects.all()
    menu_out = '<div class="CategoriesButton"><div class="CategoriesButton-title">' \
               '<div class="CategoriesButton-icon"><img src="/static/img/icons/allDep.svg" alt="allDep.svg">' \
               '</div><span class="CategoriesButton-text">All Departments</span>' \
               '<div class="CategoriesButton-arrow">' \
               '</div>' \
               '</div>' \
               '<div class="CategoriesButton-content">'
    for item in categories:
        menu_out = ''.join([menu_out, f'<div class="CategoriesButton-link"><a href="#">'
                                      f'<div class="CategoriesButton-icon"><img src="{item.icon.url}" alt="{item.name}">'
                                      f'</div><span class="CategoriesButton-text">{item.name}</span></a>'
                                      '</div>'])
    menu_out = ''.join([menu_out, '</div>'
                                  '</div><!--end CategoriesButton -->'])
    return mark_safe(menu_out)
