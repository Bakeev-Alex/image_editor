from django import template
from ..models import ArticleDetail, ImageArticle, BrandModel

register = template.Library()

"""
@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)
"""
"""
# возвращает значение для использование в шаблоне
# views убираешь все, в шаблон добавляешь {% brand_article as brands %}
@register.simple_tag(name='brand_article')
def get_brand_article():
    return BrandModel.objects.all()
"""

@register.inclusion_tag('include/brand_category.html')
def show_brand():
    brands = BrandModel.objects.all()
    return {'brands': brands}