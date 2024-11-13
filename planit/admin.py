from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Application, AdvUser

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'assigned_admin', 'status', 'created_at')
    search_fields = ('title', 'description')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Ограничиваем видимость заявок только для администраторов
        if request.user.is_superuser:
            return queryset
        return queryset.filter(assigned_admin=request.user)

    def has_change_permission(self, request, obj=None):
        # Позволяем изменять заявки только суперпользователю
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Ограничиваем выбор пользователей для поля assigned_admin
        if db_field.name == "assigned_admin":
            kwargs["queryset"] = AdvUser.objects.filter(groups__name='administrators')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AdvUser, UserAdmin) 
admin.site.register(Category)
admin.site.register(Application, ApplicationAdmin)