from django.urls import path
from . import views


urlpatterns = [
    path('painel01/', views.painel01),
    path('analise_dados/', views.analise_dados, name='data-analysis-painel01')
]