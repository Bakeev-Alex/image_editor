from django.shortcuts import render, redirect
from .models import ArticleDetail, ImageArticle
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
# Create your views here.



def index(request):
    articles = ArticleDetail.objects.all()

    page_number = request.GET.get('page')
    index_count = 2
    if request.GET.get('limit'):
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
               'is_paginated': is_paginated}
    return render(request, 'main_editor/block.html', content)


class SearchResultsView(ListView):
    model = ArticleDetail
    template_name = 'main_editor/search.html'
    paginate_by = 2


    def get_queryset(self):
        query = self.request.GET.get('q')
        articles_obj = ArticleDetail.objects.filter(Q(brand__icontains=query) | Q(article__icontains=query))
        return articles_obj

    #Формирует контекст шаблона, получаем контекст шаблона добавляем список рубрик
    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context['searchq'] = q
        return context


def delete_image(request, id):
    image =ImageArticle.objects.get(pk=id).delete()
    host = request.META.get('HTTP_REFERER')
    return redirect(host)

