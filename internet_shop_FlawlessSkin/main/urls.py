from django.urls import path, include
from . import views

# Изначально было без этого. Теперь прописывая url в шаблонах (html) нужно добавлять префикс "products:"
# Было без него и работало, но теперь так работает
app_name = 'products'

urlpatterns = [
	path('', views.index, name="index"),
	
	path('search', views.search, name="search"),
	
	path('catalog', views.CardsListView.as_view(), name="catalog"),
	# path('catalog/<int:product_id>', views.CardDetailView.as_view(), name='card_detail'),
	path('catalog/<slug:product_slug>', views.CardDetailView.as_view(), name='card_detail'),
	
	path('favourites/', views.favourites, name="favourites"),
	path('favourites/add/<int:product_id>', views.add_to_favourites, name="add_to_favourites"),
	path('favourites/remove/<int:favourites_id>', views.remove_from_favourites, name="remove_from_favourites"),
	
	path('cart/', views.cart, name="cart"),
	path('cart/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
	# важно чтобы название cart_id совпадана
	path('cart/remove/<int:cart_id>/', views.delete_for_cart, name="delete_for_cart"),
	path('cart/empty_the_cart/', views.empty_the_cart, name="empty_the_cart"),
	path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),

]
