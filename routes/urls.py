from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_route, name='add_route'),
    path('find-nth/', views.find_nth, name='find_nth'),
    path('longest/', views.longest_node, name='longest_node'),
    path('shortest-between/', views.shortest_between, name='shortest_between'),
]
