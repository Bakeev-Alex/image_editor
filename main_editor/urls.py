from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('delete-image/<int:id>/', views.delete_image, name="delete_image"),
    path('image_detail/<int:id>/', views.detail_image, name='image_detail'),
    path('brand/<int:brand_id>/', views.get_brand, name='brand_urls'),
    path('test/<int:article_id>/', views.UpdateName, name='test')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
