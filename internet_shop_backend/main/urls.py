from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="home"),
	# path('catalog', views.catalog, name="catalog"),
	path('catalog', views.CardsListView.as_view(), name="catalog"),
	path('cart/', views.cart, name="cart"),
	path('catalog/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
]

