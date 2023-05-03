from django.shortcuts import render
from .models import Product
from django.views.generic import ListView
from django.views.generic import DetailView

# Create your views here.
# функции == обработчики запросов == контроллеры (так принято нзв) == вьюхи

def index(request):
	request.session['foo'] = 'bar'
	model = Product
	products = Product.objects.all()
	# context == content == data
	context = {
		"products": products,
	}
	return render(request, 'main/index.html', context)

def cart(request):
    return render(request, "main/cart.html")

# def catalog(request):
# 	# получаем полностью все объекты
# 	products = Product.objects.all()
# 	data = {
# 		"products": products,
# 	}
# 	return render(request, 'main/catalog.html', data)

class CardsListView(ListView):
	model = Product
	template_name = "main/catalog.html"
	context_object_name = "products_list"
	# кол-во карточек на одной стронице
	paginate_by = 4
	
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
