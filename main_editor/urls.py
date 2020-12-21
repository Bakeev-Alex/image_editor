from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path(r'delete-image/(<id>\d+)/', views.delete_image, name="delete_image"),
    path('image_detail/<int:id>/', views.detail_image, name='image_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
