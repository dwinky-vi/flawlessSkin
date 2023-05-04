from django.urls import path
from . import views

# Изначально было без этого. Теперь прописывая url в шаблонах (html) нужно добавлять префикс ":products"
# Было без него и работало, но теперь так работает
app_name = 'products'

urlpatterns = [
	path('', views.index, name="index"),
	path('catalog', views.CardsListView.as_view(), name="catalog"),
	path('catalog/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
	path('cart/', views.cart, name="cart"),
]

