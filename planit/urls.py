from django.urls import path
from .views import index,ApplicationView,watchAplication
app_name = 'planit'

urlpatterns = [
    path('', index, name='index'),
    path('create_application/', ApplicationView.as_view(), name='create_application'),
    path('watch_application/', watchAplication , name='watch_application'),

]