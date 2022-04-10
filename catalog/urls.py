from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticker/', views.ticker_selected, name='ticker')
]