from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import BookCart


def checkout(request):
    cart = BookCart(request)
    if not cart:
        messages.warning(request, 'Ваш кошик порожній.')
        return redirect('shop:product_list')

    initial = {}
    if request.user.is_authenticated:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
        }
        try:
            profile = request.user.profile
            initial['city'] = profile.city
            initial['address'] = profile.address
        except Exception:
            pass

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                order.total_price = cart.get_total_price()
                order.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    product = item['product']
                    product.stock = max(0, product.stock - item['quantity'])
                    product.save()

                cart.clear()
                messages.success(
                    request,
                    f'Замовлення #{order.id} успішно оформлено! Дякуємо за покупку!'
                )
                return redirect('orders:order_detail', order_id=order.id)
        else:
            messages.error(request, 'Виправте помилки у формі.')
    else:
        form = OrderForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
    })


def order_detail(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})