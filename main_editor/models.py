from django.db import models
import os

def create_path(instance, filename):
    file_path = 'image/{}/{}'.format(instance.article, filename)
    return file_path

class ArticleDetail(models.Model):
    #article просто уникальным (unique = True), но использовать id лучше воспринимается и потом удобнее +
    article = models.IntegerField('Артикул продавца', unique=True)
    barcode = models.CharField('Штрих код', max_length=100)
    brand = models.CharField('Бренд товара', max_length=250)
    description = models.CharField('Краткое описание', max_length=400)

    class Meta:
        verbose_name_plural = 'Артикли'
        ordering = ['article']

    #
    def __str__(self):
        return str(self.article)

class ImageArticle(models.Model):
    # не писать id в базе id_id можно просто id
    article = models.ForeignKey(ArticleDetail, on_delete=models.CASCADE, related_name='image', verbose_name="article_image")
    picture_name = models.CharField('Имя изображения', max_length=100, blank=True)
    picture = models.ImageField('Изображения', upload_to=create_path, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.picture_name