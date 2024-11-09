from django.urls import path
from .views import index,ApplicationView,watchAplication,BBLoginView
app_name = 'planit'

urlpatterns = [
    path('', index, name='index'),
    path('login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', index, name='login_success' ),
    path('create_application/', ApplicationView.as_view(), name='create_application'),
    path('watch_application/', watchAplication , name='watch_application'),

]