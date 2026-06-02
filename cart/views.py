# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
# from django.http import JsonResponse
# from django.contrib import messages
# from shop.models import Product
# from .cart import BookCart


# @require_POST
# def cart_add(request, product_id):
#     cart = BookCart(request)
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))
#     override = request.POST.get('override', False)
#     cart.add(product=product, quantity=quantity, override_quantity=bool(override))
#     messages.success(request, f'"{product.name}" додано до кошика!')

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return JsonResponse({
#             'success': True,
#             'cart_count': len(cart),
#             'message': f'"{product.name}" додано до кошика!'
#         })
#     return redirect('cart:cart_detail')


# def cart_remove(request, product_id):
#     cart = BookCart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     messages.info(request, f'"{product.name}" видалено з кошика.')
#     return redirect('cart:cart_detail')


# def cart_detail(request):
#     cart = BookCart(request)
#     return render(request, 'cart/cart_detail.html', {'cart': cart})


# @require_POST
# def cart_update(request, product_id):
#     cart = BookCart(request)
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))
#     if quantity > 0:
#         cart.add(product=product, quantity=quantity, override_quantity=True)
#     else:
#         cart.remove(product)
#     return redirect('cart:cart_detail')
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from shop.models import Product
from .cart import BookCart


@require_POST
def cart_add(request, product_id):
    cart = BookCart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', 'False') == 'True'
    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f'"{product.name}" додано до кошика!')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': f'"{product.name}" додано до кошика!'
        })
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = BookCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'"{product.name}" видалено з кошика.')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = BookCart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_update(request, product_id):
    cart = BookCart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    return redirect('cart:cart_detail')