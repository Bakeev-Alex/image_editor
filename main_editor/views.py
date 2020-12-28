from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import ArticleDetail, ImageArticle, BrandModel
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageArticleForm
from django.conf import settings

import os

from django.core.exceptions import ObjectDoesNotExist


def index(request):
    articles = ArticleDetail.objects.all()
    image_size = ImageArticle.objects.all()

    page_number = request.GET.get('page')

    art_id = request.POST.get('id')
    if art_id:
        test = ImageArticle.objects.get(pk=art_id)

        if request.method == "POST":
            forms = ImageArticleForm(request.POST, instance=test)
            if forms.is_valid():
                forms.save(commit=False)
                path_name = test.picture.path
                path_image = test.picture.path.split('\\')
                del path_image[-1]
                separator = '\\'
                path_image = separator.join(path_image)
                name = path_image + '\\' + test.picture_name + '.jpg'
                os.rename(path_name, name)
                if test.picture.path != name:
                    test.picture = name
                    test.save(update_fields=['picture'])
                forms.save()
                host = request.META.get('HTTP_REFERER')
                return redirect(host)

    index_count = int(request.GET.get('limit'))
    paginator = Paginator(articles, index_count)
    try:
        pages = paginator.get_page(page_number)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = pages.page(pages.num_pages)

    is_paginated = pages.has_other_pages()

    content = {'pages': pages,
               'is_paginated': is_paginated,
               'limit': index_count,
               'image_size': image_size}
    return render(request, 'main_editor/block.html', content)


class SearchResultsView(ListView):
    model = ArticleDetail
    template_name = 'main_editor/search.html'
    context_object_name = 'article_object'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        articles_obj = ArticleDetail.objects.filter(Q(brand__brand_name__icontains=query) | Q(article__icontains=query))
        return articles_obj

    # Формирует контекст шаблона, получаем контекст шаблона добавляем список рубрик
    # Чтобы получить запрос введеный в строку поиска и присвоить значению searchq
    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context['searchq'] = q
        return context


def delete_image(request, id):
    image = ImageArticle.objects.get(pk=id).delete()
    host = request.META.get('HTTP_REFERER')
    return redirect(host)


def detail_image(request, id):
    image_detail = ImageArticle.objects.get(pk=id)
    return render(request, 'main_editor/index.html', {'image_detail': image_detail})


def get_brand(request, brand_id):
    # Верхних brand_id равен значению из таблицы ArticleDetail.brand_id
    articles_brand = ArticleDetail.objects.filter(brand_id=brand_id)
    brand = BrandModel.objects.get(pk=brand_id)

    index_count = int(request.GET.get('limit'))

    page_number = request.GET.get('page')
    paginator = Paginator(articles_brand, index_count)
    try:
        pages = paginator.get_page(page_number)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = pages.page(pages.num_pages)

    is_paginated = pages.has_other_pages()

    content = {'pages': pages,
               'brand': brand,
               'is_paginated': is_paginated,
               'index_count': index_count}
    return render(request, 'main_editor/brand.html', content)



