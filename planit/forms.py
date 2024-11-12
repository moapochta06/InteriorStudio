from django import forms
from captcha.fields import CaptchaField
from .models import Application
from django.core.exceptions import ValidationError
from .models import AdvUser
from django.contrib.auth import password_validation
from .models import user_registrated
from django import forms
from .models import AdvUser
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from .models import user_registrated


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
        if image and image.size > 2 * 1024 * 1024:  # 2MB limit
            raise forms.ValidationError("Размер изображения не должен превышать 2 МБ.")
        return image

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Выберите категорию.")
        return category

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя',  
        required=True
    )
    last_name = forms.CharField(
        label='Фамилия', 
        required=True
    )
    middle_name = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Отчество (если есть)'})
    )
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,
        help_text='Повторите тот же самый пароль еще раз'
    )
    personal_data = forms.BooleanField(
        required=True,
        label='Я согласен на обработку персональных данных',
        error_messages={'required': 'Необходимо согласие на обработку данных.'}
    )

    captcha = CaptchaField(label='Введите код с картинки')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Введенные пароли не совпадают.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  
        user.is_activated = False  
        if commit:
            user.save()
            user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username','last_name', 'middle_name', 'email', 'password1', 'password2','personal_data','captcha')


class UpdateApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'image', 'comment']  

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        image = cleaned_data.get('image')
        comment = cleaned_data.get('comment')

        if self.instance.status == 'new':
            if status == 'completed' and not image:
                raise forms.ValidationError("При смене статуса на 'Выполнено' необходимо прикрепить изображение.")
            if status == 'in_progress' and not comment:
                raise forms.ValidationError("При смене статуса на 'Принято в работу' необходимо указать комментарий.")

        if self.instance.status == 'in_progress':
            if status == 'completed' and not image:
                raise forms.ValidationError("При смене статуса на 'Выполнено' необходимо прикрепить изображение.")

        if self.instance.status in ['completed']:
            raise forms.ValidationError("Смена статуса невозможна с текущего состояния.")

        return cleaned_data