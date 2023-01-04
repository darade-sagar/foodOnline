from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.newsFeed, name='newsFeed'),
    path('add-news', views.addNews, name='addNews'),
    path('full-news/<slug:news_slug>', views.fullNews, name='fullNews'),
    path('update-news/<slug:news_slug>', views.updateNews, name='updateNews'),
    path('delete/<int:news_id>', views.deleteNews, name='deleteNews'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]