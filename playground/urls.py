from django.urls import path
from . import views
urlpatterns = [
    path('hello/', views.say_hello, name='say_hello'),
    path('visualize/pathfind/', views.pathfind, name='pathfind'),
    path('get_current_time/',views.get_current_time,name='get_current_time')
]