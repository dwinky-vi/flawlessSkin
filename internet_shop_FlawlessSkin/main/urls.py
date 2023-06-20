from django.urls import path, include
from . import views

# Изначально было без этого. Теперь прописывая url в шаблонах (html) нужно добавлять префикс "products:"
# Было без него и работало, но теперь так работает
app_name = 'products'

urlpatterns = [
	path('', views.index, name="index"),
	
	path('subscribe', views.subscribe_ajax, name="subscribe"),

	path('search', views.search, name="search"),
	path('find', views.search_processing_by_ajax, name="search_processing_by_ajax"),

	path('catalog', views.CardsListView.as_view(), name="catalog"),
	path('catalog/<slug:product_slug>', views.CardDetailView.as_view(), name='card_detail'),

	path('favourites/', views.favourites, name="favourites"),
	path('favourites/add/<int:product_id>', views.add_to_favourites, name="add_to_favourites"),
	path('favourites/remove/<int:product_id>', views.remove_from_favourites, name="remove_from_favourites"),
	# важно чтобы название product_id совпадана с view

	path('cart/', views.cart, name="cart"),
	path('cart/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
	path('cart/remove/<int:product_id>/', views.delete_from_cart, name="delete_from_cart"),
	path('cart/empty_the_cart/', views.empty_the_cart, name="empty_the_cart"),
	path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),

	path('order/make/', views.make_order, name="make_order"),
	# path('order/save/', views.save_order, name="save_order"),
]
