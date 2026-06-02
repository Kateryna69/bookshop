from .cart import BookCart


def cart(request):
    return {'cart': BookCart(request)}