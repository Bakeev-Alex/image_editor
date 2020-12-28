from django.db import models
from django.urls import reverse



def create_path(instance, filename):
    file_path = 'image/{}/{}'.format(instance.article, filename)
    return file_path

class BrandModel(models.Model):
    brand_name = models.CharField('Бренд', max_length=200)

    def __str__(self):
        return self.brand_name

class ArticleDetail(models.Model):
    # article просто уникальным (unique = True), но использовать id лучше воспринимается и потом удобнее +
    article = models.IntegerField('Артикул продавца', unique=True)
    barcode = models.CharField('Штрих код', max_length=100)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, related_name='brand',
                                verbose_name="article_brand")
    description = models.CharField('Краткое описание', max_length=400)

    class Meta:
        verbose_name_plural = 'Артикли'
        ordering = ['article']

    def __str__(self):
        return str(self.article)



class ImageArticle(models.Model):
    # не писать id в базе id_id можно просто id
    article = models.ForeignKey(ArticleDetail, on_delete=models.CASCADE, related_name='image',
                                verbose_name="article_image")
    picture_name = models.CharField('Имя изображения', max_length=100, blank=True)
    picture = models.ImageField('Изображения', upload_to=create_path, blank=True)
    """
    def save(self, *args, **kwargs):
        if self.article:
            self.picture = self.picture_name
        else:
            self.picture_name = create_path
        super(ImageArticle, self).save(*args, **kwargs)
    """

    class Meta:
        verbose_name_plural = 'Изображения'
        ordering = ['article']

    def __str__(self):
        return str(self.picture_name)

    def get_absolute_url(self):
        return reverse('test', args=[self.id])
