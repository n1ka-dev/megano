import urllib

from django import template
from django.db.models import Sum, F, Case, When, Count
from django.utils.safestring import mark_safe

from app_shop.models import Category, Tags

register = template.Library()
SORT_VALUES = {
    'popular': 'Популярности',
    'price': 'Цене',
    'reviews': 'Отзывам',
    'create_date': 'Новизне'
}


@register.simple_tag(takes_context=True)
def get_sort_block(context, *args, **kwargs):
    q_items = context.request.GET
    general_get = {item: ';'.join(val) for item, val in dict(q_items).items() if 'sort_' not in item}
    general_get = urllib.parse.urlencode(general_get)
    general_get == ''
    if general_get:
        general_get += '&'
    cur_sort_field = context.request.GET.get('sort_field', 'popular')
    cur_sort_by = context.request.GET.get('sort_by', 'dec')
    out_str = '<div class="Sort-variants">'
    for option_name, display_name in SORT_VALUES.items():
        order_disp = ''
        if option_name == cur_sort_field:
            order = 'inc' if cur_sort_by == 'dec' else 'dec'
            order_disp = 'inc' if order == 'dec' else 'dec'
            sort_by = f"&sort_by={order}"
        else:
            sort_by = f"&sort_by=dec"

        out_str += f'<a class="Sort-sortBy Sort-sortBy_{order_disp}" href="?{general_get}sort_field={option_name}{sort_by}">{display_name}</a>'

    out_str += '</div>'

    return mark_safe(out_str)


@register.simple_tag(takes_context=True)
def get_cloud_tags(context, tags, *args, **kwargs):

    tags_l = []

    cur_gets = context.request.GET  # если уже есть фильтрация, то не сбрасываем ее

    cur_gets_str = '&'.join([f'{key}={val}' for key, val in cur_gets.items() if key != 'tag'])
    for tag in tags:
        tag = tag['tags__name']
        status = ''
        tag_url = f'&tag={tag}'
        if cur_gets:
            if 'tag' in cur_gets and str(tag) in cur_gets['tag']:
                status = ' active'
                tag_url = ''

            tags_l.append(
                f'<a class="btn btn_default btn_sm{status}" href="?{cur_gets_str}{tag_url}">{tag}</a>')
        else:
            tags_l.append(
                f'<a class="btn btn_default btn_sm" href="?tag={tag}">{tag}</a>')

    out_str = ''.join(tags_l)
    return mark_safe(out_str)


@register.simple_tag(takes_context=True)
def get_catalog_menu(context, *args, **kwargs):
    categories = Category.objects.filter(parent_category__isnull=True).annotate(
        count_subitems=Count('parent')
    )
    menu_out = '<div class="CategoriesButton"><div class="CategoriesButton-title">' \
               '<div class="CategoriesButton-icon"><img src="/static/img/icons/allDep.svg" alt="allDep.svg">' \
               '</div><span class="CategoriesButton-text">All Departments</span>' \
               '<div class="CategoriesButton-arrow">' \
               '</div>' \
               '</div>' \
               '<div class="CategoriesButton-content">'
    for item in categories:
        new_item = f'<a href="{item.get_absolut_url()}"><div class="CategoriesButton-icon"><img src="{item.icon.url}" alt="{item.name}"></div>' \
                   f'<span class="CategoriesButton-text">{item.name}</span></a>'
        sub_item_menu = ''
        if item.count_subitems:
            new_item += '<a class="CategoriesButton-arrow" href="#"></a>'
            sub_items = ''
            for sub_item in item.parent.all():
                sub_items = f'{sub_items}<a class="CategoriesButton-link" href="{sub_item.get_absolut_url()}">' \
                            f'<div class="CategoriesButton-icon">' \
                            f'<img src="{sub_item.icon.url}" alt="{sub_item.name}">' \
                            f'</div><span class="CategoriesButton-text">{sub_item.name}</span>' \
                            f'</a>'
            sub_item_menu = f'<div class="CategoriesButton-submenu">{sub_items}</div>'
        menu_out = ''.join([menu_out, '<div class="CategoriesButton-link">', new_item, sub_item_menu, '</div>'])
    menu_out = ''.join([menu_out, '</div>'
                                  '</div><!--end CategoriesButton -->'])
    return mark_safe(menu_out)
