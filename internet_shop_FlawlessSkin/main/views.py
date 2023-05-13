from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import ProductCategory, Product, Cart, Favourites
from users.forms import User, UserProfileForm
# from users.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

# Create your views here.
# функции == обработчики запросов == контроллеры (так принято нзв) == вьюхи

def index(request):
	request.session['foo'] = 'bar'
	# model = Product
	products = Product.objects.all()
	products_sort = Product.objects.order_by('-date')[:8]
	categories = ProductCategory.objects.all()
	# context == content == data
	context = {
		"products": products_sort,
		"categories": categories,
	}
	return render(request, 'main/index.html', context)
	

@login_required
def favourites(request):
	context = {
		"favourites": Favourites.objects.filter(user=request.user).order_by('-created_timestamp'),
	}
	return render(request, "main/favourites.html", context)

@login_required
def add_to_favourites(request, product_id):
	product = Product.objects.get(id=product_id)
	favourite = Favourites.objects.filter(user=request.user, product=product)
	if not favourite.exists():
		Favourites.objects.create(user=request.user, product=product)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# Корзина
@login_required
def cart(request):
	# кажется эта форма не нужна здесь
	# в 9-ом видео курса по django он использует корзину в профиле, поэтому скорее всего я скопипастил со своего профиля
	# if request.method == "POST":
	# 	form = UserProfileForm(instance=request.user, data=request.POST)
	# 	if form.is_valid():
	# 		form.save()
	# 		return HttpResponseRedirect(reverse('users:profile'))
	# 	else:
	# 		print("profile:", form.errors)
	# else:
	# 	form = UserProfileForm(instance=request.user)
	
	carts = Cart.objects.filter(user=request.user)
	# total_amount = sum(cart.total_price() for cart in carts)
	# total_quantity = sum(cart.quantity for cart in carts)

	context = {
		# 'form': form,
		'carts': carts,
		# 'total_amount': carts.total_amount(),
		# 'total_quantity': carts.total_quantity(),
	}
	return render(request, "main/cart.html", context)

class CardsListView(ListView):
	model = Product
	template_name = "main/catalog.html"
	context_object_name = "products_list"
	paginate_by = 8
	
	def get_queryset(self):
		qs = Product.objects.order_by('date')
		return qs


class CardDetailView(DetailView):
	model = Product
	template_name = "main/card_detail.html"
	context_object_name = "product"
	slug_field = "one"

	def get_context_data(self, **kwargs):
		context = super(CardDetailView, self).get_context_data(**kwargs)
		return context
	
	# с хабра https://habr.com/ru/articles/137530/
	# работает также как наверху
	# def get_object(self):
	# 	object = super(CardDetailView, self).get_object()
	# 	Для неавторизованного пользователя возвращает 404 ошибку
	# 	if not self.request.user.is_authenticated():
	# 		raise Http404
	# 	return object

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

@login_required
def delete_for_cart(request, cart_id):
	cart = Cart.objects.get(id=cart_id)
	cart.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_all_carts_for_user(request, cart_id):
	cart = Cart.objects.get(id=cart_id)
	cart.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))