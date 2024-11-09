from django import forms
from .models import Application, Category
from django.core.exceptions import ValidationError

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Это поле обязательно для заполнения.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Это поле обязательно для заполнения.")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Размер изображения не должен превышать 2 МБ.")
            return image
        else:
            raise forms.ValidationError("Это поле обязательно для заполнения.")

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Выберите категорию.")
        
        return category