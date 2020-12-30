from django.contrib import admin
from .models import *

class ProductImagesInline(admin.StackedInline):
    model = ImageArticle
    extra = 2


@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ['article', 'barcode', 'brand', 'description']
    search_fields = ('pk', 'brand__brand_name', 'barcode')

    inlines = [ProductImagesInline]



@admin.register(BrandModel)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name',]

