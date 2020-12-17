from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path(r'delete-image/(<id>\d+)/', views.delete_image, name="delete_image"),
]
