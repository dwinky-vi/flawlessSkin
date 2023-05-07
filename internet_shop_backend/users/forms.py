from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User
from django import forms


# класс отвечает за работу с формой
class UserLoginForm(AuthenticationForm):
	# label = 'Вход'
	username = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control', "placeholder": "Введите почту"}))
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control', "placeholder": "Введите пароль"}))
	
	class Meta:
		# указываем. что данный класс (форма) работает модель пользователей
		model = User
		# и конкретно с полями: (можно использовать и корртеж -- [])
		fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
	# label = 'Регистрация'
	username = forms.CharField(widget=forms.EmailInput(attrs={
		'class': 'form-control', "placeholder": "Введите почту"}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control', "placeholder": "Введите пароль"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control', "placeholder": "Повторите пароль"}))
	
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
	# required=False
	# значит, что поле не обязательно для заполнения
	username = forms.CharField(widget=forms.TextInput(attrs={
		"class": "profile__input validate", "type": "text", "placeholder": " ",
		"readonly": "True",
	}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "profile__input validate", "type": "text", "placeholder": " ",
	}), required=False)
	last_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "profile__input validate", "type": "text", "placeholder": " ",
	}), required=False)
	phone = forms.CharField(widget=forms.TextInput(attrs={
		"class": "profile__input validate", "type": "tel", "placeholder": " ",
	}), required=False)
	# email = forms.CharField(widget=forms.EmailInput(attrs={
	# 	"class": "profile__input validate", "type": "email", "placeholder": " ",
	# }))
	address = forms.CharField(widget=forms.TextInput(attrs={
		"class": "profile__input validate", "type": "text", "placeholder": " ",
	}), required=False)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'phone', 'email', 'address')
