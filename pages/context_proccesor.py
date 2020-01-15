from mixture.models import Cart, CartItem

def get_cart(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
	except Exception as e:
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
	return(cart)


def cart_count(request):
	cart    = get_cart(request)
	items	= CartItem.objects.filter(cart=cart, ordered=False)
	if items:
		return{"cart_count": items.count()}
	else:
		return{"cart_count": None}

def get_total_price(request):
	total_price = 0
	cart       =  Cart.objects.get(
		id          = request.session['cart_id'],
		ordered     = False)
	items   = CartItem.objects.filter(
		cart    = cart,
		ordered = False
	)
	for item in items:
		total_price += item.get_total_clear_price()
	return total_price