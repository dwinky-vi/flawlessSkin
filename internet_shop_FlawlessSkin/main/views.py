from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from .models import ProductCategory, Product, Cart, Favourites
from users.forms import User, UserProfileForm
# from users.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
# функции == обработчики запросов == контроллеры (так принято нзв) == вьюхи

# Главная страница
def index(request):
	request.session['foo'] = 'bar'
	products_sort = Product.objects.order_by('-date')[:8]
	categories = ProductCategory.objects.all()
	favourites_products_list = list()
	for item in Favourites.objects.filter(user=request.user):
		favourites_products_list.append(item.product)
	# context == content == data
	context = {
		"products": products_sort,
		"categories": categories,
		"favourites_products_list": favourites_products_list,
	}
	return render(request, 'main/index.html', context)
	
	
	
	# Поиск
def search(request):
	products_sort = Product.objects.order_by('-date')
	categories = ProductCategory.objects.all()
	# context == content == data
	context = {
		"products": products_sort,
		"categories": categories,
	}
	return render(request, 'main/search_page.html', context)
	
	
	# Страница избранное
@login_required
def favourites(request):
	favourites = Favourites.objects.filter(user=request.user).order_by('-created_timestamp')
	context = {
		"favourites": favourites,
	}
	return render(request, "main/favourites.html", context)
	
	# Добавление в избранное
@login_required
def add_to_favourites(request, product_id):
	product = Product.objects.get(id=product_id)
	favourite = Favourites.objects.filter(user=request.user, product=product)
	if not favourite.exists():
		Favourites.objects.create(user=request.user, product=product)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	# Удаление из избранное
@login_required
def remove_from_favourites(request, favourites_id):
	# product = Product.objects.get(id=product_id)
	favourite = Favourites.objects.get(id=favourites_id)
	favourite.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	# Корзина
@login_required
def cart(request):
	carts = Cart.objects.filter(user=request.user)
	# total_amount = sum(cart.total_price() for cart in carts)
	# total_quantity = sum(cart.quantity for cart in carts)
	
	context = {
		'carts': carts,
		# 'total_amount': carts.total_amount(),
		# 'total_quantity': carts.total_quantity(),
	}
	return render(request, "main/cart.html", context)
	
	
	# Добавление в корзину
# контролер обработчик событий
# @login_required(login_url='/users/login/') # декаратор доступа. Выполнеяется до выполнения основной логии функции
@login_required  # декаратор доступа. Выполнеяется до выполнения основной логии функции
def add_to_cart(request, product_id):
	# можно так сделать проверку, если пользователь не авторизован
	if request.user.is_authenticated:
		product = Product.objects.get(id=product_id)
		# возьмутся все корзины пользователя с определеным продуктом
		# вернётся список с одним продуктом
		cart = Cart.objects.filter(user=request.user, product=product)
		if not cart.exists():
			Cart.objects.create(user=request.user, product=product, quantity=1)
		else:
			cart = cart.first()
			cart.quantity += 1
			cart.save()
		# возвращаем пользователя на ту страницу, где он находится
		# HTTP_REFERER -- та страница, где находится пользователь
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	
	# Удаление из корзины
@login_required
def delete_for_cart(request, cart_id):
	cart = Cart.objects.get(id=cart_id)
	cart.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	# Удаление всей корзины
@login_required
def empty_the_cart(request):
	carts = Cart.objects.filter(user=request.user)
	for cart in carts:
		cart.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	# Изменение штук товара в корзине
def update_cart_quantity(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		cart_id = data.get('cart_id')
		new_quantity = data.get('new_quantity')
		cart = Cart.objects.get(id=cart_id)
		cart.quantity = new_quantity
		cart.save()
		
	
		# Возвращение JSON-ответа об успешном обновлении
		return JsonResponse({'success': True})

	# Обработка других методов запроса, если необходимо
	return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Каталог
class CardsListView(ListView):
	model = Product
	template_name = "main/catalog.html"
	context_object_name = "products_list"
	# extra_context = "list_in_cart"
	paginate_by = 8
	
	def get_queryset(self):
		qs = Product.objects.order_by('date')
		return qs
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['favourites'] = Favourites.objects.filter(user=self.request.user)
		context['favourites_products_list'] = list()
		if self.request.user.is_authenticated:
			for item in Favourites.objects.filter(user=self.request.user):
				context['favourites_products_list'].append(item.product)
		return context
	
	# Страница с детальной информацией о продукте
class CardDetailView(DetailView):
	model = Product
	template_name = "main/card_detail.html"
	context_object_name = "product"
	# slug_field = "product_slug"
	slug_url_kwarg = "product_slug"
	
	# query_pk_and_slug = "slug"
	# pk_url_kwarg = "product_id"
	# slug_field = "slug"
	
	def get_context_data(self, **kwargs):
		context = super(CardDetailView, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context["is_favourite"] = False
			fav_prod = Favourites.objects.filter(user=self.request.user, product=context["product"])
			if fav_prod.exists():
				context["is_favourite"] = True
		return context

# с хабра https://habr.com/ru/articles/137530/
# работает также как наверху
# def get_object(self):
# 	object = super(CardDetailView, self).get_object()
# 	Для неавторизованного пользователя возвращает 404 ошибку
# 	if not self.request.user.is_authenticated():
# 		raise Http404
# 	return object

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1> страница не найдена </h1>')