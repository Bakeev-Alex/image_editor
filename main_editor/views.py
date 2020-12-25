from django.shortcuts import render, redirect, get_object_or_404
from .models import ArticleDetail, ImageArticle, BrandModel
from django.db.models import Q
from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageArticleForm


"""
def ImageNameForm(request, picture_name):
    example_form_set = modelformset_factory(ImageArticle, fields=('picture_name',))
    form = example_form_set()
    return render(request, 'main_editor/block.html', {'form': form})
"""

def index(request):
    articles = ArticleDetail.objects.all()
    image_size = ImageArticle.objects.all()


    page_number = request.GET.get('page')
    limit = request.GET.get('limit')
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
               'limit': limit,
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

def UpdateName(request, article_id):
    post = get_object_or_404(ArticleDetail, pk=article_id)
    post_image = ImageArticle.objects.filter(article_id=article_id)
    query = request.POST.get('forms')
    print(query)
    forms = ImageArticleForm()
    if request.method == 'POST':
        forms = ImageArticleForm(request.POST)
        if forms.is_valid():
            forms.save()
    return render(request, 'main_editor/test.html', {'post': post,
                                                     'post_image': post_image,
                                                     'forms': forms,
                                                     'query': query})
