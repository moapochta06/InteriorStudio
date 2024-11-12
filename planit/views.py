from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application,AdvUser,Category
from .forms import ApplicationForm,RegisterUserForm,UpdateApplicationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.signing import BadSignature

from .utilities import signer

def index(request):
    applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()
    return render(request, 'application/watch_application.html', {
        'applications': applications,
        'is_index_page': True,
        'in_progress_count': in_progress_count
    })

class RegisterUserView(CreateView):
   model = AdvUser
   template_name = 'user/register_user.html'
   form_class = RegisterUserForm
   success_url = reverse_lazy('planit:register_done')


class RegisterDoneView(TemplateView):
   template_name = 'user/register_done.html'

def user_activate(request, sign):
   try:
       username = signer.unsign(sign)
   except BadSignature:
       return render(request, 'user/bad_signature.html')
   user = get_object_or_404(AdvUser, username=username)
   if user.is_activated:
       template = 'user/user_is_activated.html'
   else:
       template = 'user/activation_done.html'
       user.is_activated = True
       user.is_active = True
       user.save()
   return render(request, template)


class BBLoginView(LoginView):
    template_name = 'user/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему!")
        return super().form_valid(form)

class BBLogoutConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/confirm_logout.html')
        
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'user/logged_out.html'



class ApplicationView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application/create_application.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        messages.success(self.request, 'Заявка успешно создана!')
        return super().form_valid(form)
    
class WachApplication(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'application/watch_application.html'  
    context_object_name = 'applications' 

    def get_queryset(self):
            if self.request.user.is_staff:
                queryset = Application.objects.all()  
            else:
                queryset = Application.objects.filter(user=self.request.user) 
            status_filter = self.request.GET.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Application.STATUS_CHOICES
        context['is_index_page'] = False  
        return context

class UpdateApplicationStatusView(LoginRequiredMixin, UpdateView):
    model = Application
    form_class = UpdateApplicationForm
    template_name = 'application/update_application.html'  
    success_url = reverse_lazy('planit:watch_application')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "У вас нет прав для изменения статуса заявки.")
            return redirect('planit:watch_application')  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.object.user 
        
        messages.success(self.request, 'Статус заявки успешно обновлён!')
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(user=self.request.user)


class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'application/application_confirm_delete.html'  
    success_url = reverse_lazy('planit:watch_application') 

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(user=self.request.user)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/category_list.html' 
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'category/category_form.html'  
    success_url = reverse_lazy('planit:category_list')  

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно добавлена.")
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'  
    success_url = reverse_lazy('planit:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        applications_count = Application.objects.filter(category=category).count()
        Application.objects.filter(category=category).delete()  
        
        messages.success(request, f'Категория "{category.name}" и все связанные заявки (всего {applications_count}) успешно удалены.')
        return super().delete(request, *args, **kwargs)