from django.urls import path
from .views import index,ApplicationView,WatchAplication,BBLoginView, BBLogoutView,BBLogoutConfirmationView,ApplicationDelete,RegisterUserView,RegisterDoneView,user_activate
app_name = 'planit'

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', index, name='login_success' ),
    path('logout/confirm/', BBLogoutConfirmationView.as_view(), name='logout_confirm'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
    path('create_application/', ApplicationView.as_view(), name='create_application'),
    path('watch_application/', WatchAplication.as_view() , name='watch_application'),
    path('application/<int:pk>/delete/', ApplicationDelete.as_view() , name='delete_application'),

]