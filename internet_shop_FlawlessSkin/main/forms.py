from .models import Order, Product
from django import forms

class OrderForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ",
	}), required=True)  # required значит что поле должно быть обязательно заполнено
	last_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ",
	}), required=False)
	phone = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "tel", "placeholder": " ",
	}), required=False)
	email = forms.CharField(widget=forms.EmailInput(attrs={
		"class": "input_data", "type": "email", "placeholder": " ",
	}))
	address = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ", "id": "address",
	}), required=False)
	
	class Meta:
		model = Order
		fields = ('first_name', 'last_name', 'phone', 'email', 'address')


def make_order(request):
	try:
		user = request.user
	except ObjectDoesNotExist:
		print("Пользователь не найден.")
		return redirect('products:cart')
	
	carts = Cart.objects.filter(user=user)
	if carts.count() == 0:
		print(f"Корзина пуста.")
		return redirect('products:cart')
	
	products = [cart.product for cart in carts]
	total_sum = carts.first().total_amount()
	
	if "order" in request.session:
		print(f"session is active")
		total_sum2 = request.session["total_sum"]
		print(f"ses: {total_sum}, {total_sum2}")
	# carts = request.session['carts']
	# products = request.session['products']
	else:
		request.session["order"] = True
		request.session["total_sum"] = total_sum
		print(f"session no active")
	
	# Store carts and products in the session
	# request.session['carts'] = carts
	# request.session['products'] = products
	# request.session['total_sum'] = total_sum
	
	if request.method == 'POST':
		form = OrderForm(data=request.POST)
		if form.is_valid():
			order = form.save(commit=False)  # Создаем объект Order, но не сохраняем его в базе данных пока
			order.user = user
			# order.sum = request.session['total_sum']
			order.sum = total_sum
			order.save()  # Теперь сохраняем объект Order в базе данных
			# важно сначала сохранить модель, а потом добавлять продукты
			# иначе возникнет ошибку, что потому мы пытаемся добавить связь "многие-ко-многим"
			# между объектом Order и продуктами до сохранения объекта Order в базе данных.
			# order.products.set(request.session["products"])
			order.products.set(products)
			carts.delete()  # Удаляем товары из корзины
			# del request.session['carts']  # Remove carts from session
			# del request.session['products']  # Remove products from session
			del request.session['order']
			del request.session['total_sum']
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
