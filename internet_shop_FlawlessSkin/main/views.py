from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from .models import ProductCategory, Product, Cart, Favourites, Order, Contact
from .forms import OrderForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.core import serializers

# функции == обработчики запросов == контроллеры (так принято нзв) == вьюхи

	# Главная страница
def index(request):
	# request.session['foo'] = 'bar'
	products_sort = Product.objects.order_by('-date')[:8]
	categories = ProductCategory.objects.all()
	favourites_products = list()
	products_in_cart = list()
	if request.user.is_authenticated:
		for item in Favourites.objects.filter(user=request.user):
			favourites_products.append(item.product)
		for item in Cart.objects.filter(user=request.user):
			products_in_cart.append(item.product)
	else:
		pass
	# context == content == data
	context = {
		"products": products_sort,
		"categories": categories,
		"products_in_cart": products_in_cart,
		"favourites_products": favourites_products,
	}
	return render(request, 'main/index.html', context)
	
	# email-рассылка
def subscribe_ajax(request):
	email_to_subscribe = request.GET.get('email')
	if Contact.objects.filter(email=email_to_subscribe).exists():
		print("Email already exists")
		return JsonResponse({'error': 'Вы уже были подписанны на рассылку писем'})  # Возвращаем Json объект
	else:
		Contact.objects.create(email=email_to_subscribe)
		return JsonResponse({'success': True})
	# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# Поиск
def search(request):
	products = Product.objects.all()
	categories = ProductCategory.objects.all()
	favourites_products = list()
	products_in_cart = list()
	
	products_from_search = Product.objects.order_by('-date')
	
	if request.user.is_authenticated:
		for item in Favourites.objects.filter(user=request.user):
			favourites_products.append(item.product)
		for item in Cart.objects.filter(user=request.user):
			products_in_cart.append(item.product)
	
	# context == content == data
	context = {
		"products": products,
		"products_from_search": products_from_search,
		"favourites_products": favourites_products,
		"products_in_cart": products_in_cart,
		"categories": categories,
		"hello": "12345",
	}
	return render(request, 'main/search_page.html', context)



class CustomJSONEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()
		return super().default(obj)
	
	# Отправка поискового запроса
def search_processing_by_ajax(request):
	search_string = request.GET.get('search_string')
	search_string_split = search_string.split()
	products_from_search = list(Product.objects.filter(title=search_string).values())
	print(f'1) {products_from_search}')
	
	print(f'result = {products_from_search}')
	data = json.dumps(products_from_search, cls=CustomJSONEncoder)
	
	# Параметр safe = False указывает, что передаваемый аргумент data уже является строкой JSON и не требует дополнительного преобразования.
	return JsonResponse(data, safe=False)
	# return JsonResponse({'success': True, 'products_id_from_search': products_id_from_search})
	# return render(request, 'main/search_page.html')


	# Страница избранное
@login_required
def favourites(request):
	favourites = Favourites.objects.filter(user=request.user).order_by('-created_timestamp')
	products_in_cart = list()
	for item in Cart.objects.filter(user=request.user):
		products_in_cart.append(item.product)
	context = {
		"favourites": favourites,
		"products_in_cart": products_in_cart,
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
def remove_from_favourites(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
		favourite = Favourites.objects.filter(user=request.user, product=product)
	except ObjectDoesNotExist:
		# Обработка случая, когда объект не найден
		print("Корзина не найдена.")
		return redirect('products:favourites')
	
	favourite = favourite.first()
	favourite.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# Корзина
@login_required
def cart(request):
	carts = Cart.objects.filter(user=request.user)
	context = {
		'carts': carts,
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
def delete_from_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart = Cart.objects.get(user=request.user, product=product)
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
		context['favourites_products'] = list()
		context['products_in_cart'] = list()
		if self.request.user.is_authenticated:
			for item in Favourites.objects.filter(user=self.request.user):
				context['favourites_products'].append(item.product)
			for item in Cart.objects.filter(user=self.request.user):
				context['products_in_cart'].append(item.product)
		return context
	
	# Страница с детальной информацией о продукте
class CardDetailView(DetailView):
	model = Product
	template_name = "main/card_detail.html"
	context_object_name = "product"
	slug_url_kwarg = "product_slug"

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

def make_order(request):
	# request.session.flush()
	try:
		user = request.user
		if not user.is_authenticated:
			print("ПОЛЬЗОВАТЕЛЬ НЕ АВТОРИЗОВАН")
	except ObjectDoesNotExist:
		print("Пользователь не найден.")
		return redirect('products:cart')
	except Exception as e:
		print(f"Произошла ошибка: {str(e)}")
		return redirect('products:cart')

	if "order" in request.session:
		total_sum = request.session.get("total_sum")
		products_id = request.session.get("products_id")
		products = list()
		for product_id in products_id:
			p = Product.objects.get(id=product_id)
			products.append(p)

		carts_id = request.session.get("carts_id")
		carts = Cart.objects.none()
		for cart_id in carts_id:
			carts = carts | Cart.objects.filter(id=cart_id)
	else:
		request.session["order"] = True

		carts = Cart.objects.filter(user=user)
		if carts.count() == 0:
			print(f"Корзина пуста.")
			return redirect('products:cart')

		total_sum = carts.first().total_amount()
		request.session["total_sum"] = total_sum
		products = [cart.product for cart in carts]
		products_id = list()
		for product in products:
			products_id.append(product.id)
		request.session['products_id'] = products_id

		carts_id = list()
		for cart in carts:
			carts_id.append(cart.id)
		request.session['carts_id'] = carts_id
		print(f"session no active")

	# перенести сохранения ссесии в не POST запрос
	# если пользователь не закончит оформление заказа и начнет новую -- будет ошибка
	if request.method == 'POST':
		form = OrderForm(data=request.POST)
		if form.is_valid():
			order = form.save(commit=False)  # Создаем объект Order, но не сохраняем его в базе данных пока
			order.user = user
			order.sum = total_sum
			order.save()  # Теперь сохраняем объект Order в базе данных
			# важно сначала сохранить модель, а потом добавлять продукты
			# иначе возникнет ошибку, что потому мы пытаемся добавить связь "многие-ко-многим"
			# между объектом Order и продуктами до сохранения объекта Order в базе данных.
			# order.products.set(request.session["products"])
			order.products.set(products)
			carts.delete()  # Удаляем товары из корзины
			del request.session['order']
			del request.session['total_sum']
			del request.session['products_id']
			del request.session['carts_id']
			return redirect('products:cart')
	else:
		initial_data = {
			"first_name": user.first_name,
			"last_name": user.last_name,
			"phone": user.phone,
			"email": user.username,
			"address": user.address,
		}
		form = OrderForm(initial=initial_data)
		
	context = {
		'form': form,
		'products': products,
		'total_sum': total_sum,
	}
	return render(request, "main/make_order.html", context)
#
# def save_order(request):
# 	if request.method == 'POST':
# 		form = OrderForm(data=request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('products:cart')
#
# 	else:
# 		form = OrderForm()
# 	context = {
# 		'form': form,
# 	}
# 	# carts = Cart.objects.filter(user=request.user)
# 	# products = [cart.product for cart in carts]
# 	# total_sum = carts.first().total_amount()
# 	# order = Order.objects.create(user=request.user, sum=total_sum)
# 	# order.products.set(products)
# 	# order.save()
# 	return render(request, "main/make_order.html", context)
