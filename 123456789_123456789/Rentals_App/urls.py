from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('query_results/', views.query_results, name='query_results'),
    path('add_rental/', views.add_rental, name='add_rental'),
    path('search_analysis/', views.search_analysis, name='search_analysis'),
]
