from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from .models import Application
from .forms import ApplicationForm
from django.urls import reverse_lazy
from django.contrib import messages
import os


def watchAplication(request):
    applications = Application.objects.all().order_by('-created_at')
    return render(request, 'application/watch_application.html',
    {'applications': applications})

def index(request):
    applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    return render(request, 'application/watch_application.html', {'applications': applications})

class ApplicationView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application/create_application.html'
    success_url = '/'  

    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем текущего пользователя как автора заявки
        messages.success(self.request, 'Заявка успешно создана!')
        return super().form_valid(form)