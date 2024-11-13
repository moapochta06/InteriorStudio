from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification
user_registrated = Signal('instance')

class AdvUser(AbstractUser): 
    middle_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    is_activated = models.BooleanField(default=True, 
    db_index=True, verbose_name='Прошел активацию?') 
    personal_data = models.BooleanField(default=True, 
    verbose_name='Я согласен на обработку персональных данных',null=False, blank=False) 
class Meta(AbstractUser.Meta): 
    pass

def user_registrated_dispatcher(sender, **kwargs):
   send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='applications/', null=True, blank=True, verbose_name='Изображение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    assigned_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_applications', verbose_name='Назначенный администратор')
    def __str__(self):
        return self.title
    
class ApplicationChangeHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='change_history')
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.application.title} changed from {self.previous_status} to {self.new_status} on {self.changed_at}"


