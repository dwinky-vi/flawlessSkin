from django.urls import path
from . import views

# Изначально было без этого. Теперь прописывая url в шаблонах (html) нужно добавлять префикс ":products"
# Было без него и работало, но теперь так работает
app_name = 'users'

urlpatterns = [
	path('login_old/', views.login_old, name="login_old"),
	path('login/', views.login, name="login"),
	path('registration/', views.registration, name="registration"),
	path('profile/', views.profile, name="profile"),
	path('logout/', views.logout, name="logout"),
]

