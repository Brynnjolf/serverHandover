from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter, name='filter'),
    path('table/', views.table, name='table'),
    path('update', views.update, name='update'),
    path('postfilter', views.postfilter, name='postfilter'),
    path('api/getPriceData/<str:ticker>/', views.getPriceData, name='priceData'),
    path('<str:ticker>/', views.summary, name='summary'),
]   
