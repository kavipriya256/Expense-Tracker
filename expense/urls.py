from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chart-data/', views.chart_data, name='chart_data'),
]
