from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, Wishlist


def product_list(request, category_slug=None):
    categories = Category.objects.filter(parent=None).prefetch_related('children')
    products = Product.objects.filter(available=True).select_related('category')
    featured = Product.objects.filter(is_featured=True, available=True)[:8]
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )

    sort = request.GET.get('sort', '')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'rating': '-rating',
        'new': '-created',
    }
    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(
                user=request.user
            ).values_list('product_id', flat=True)
        )

    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'products': products,
        'featured': featured,
        'current_category': current_category,
        'query': query,
        'sort': sort,
        'wishlist_ids': wishlist_ids,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug, available=True
    )
    related = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, product=product
        ).exists()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
        'in_wishlist': in_wishlist,
    })


@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        wishlist_item.delete()
        added = False
        messages.info(request, f'"{product.name}" видалено з бажаного.')
    else:
        added = True
        messages.success(request, f'"{product.name}" додано до бажаного!')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'added': added})

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(
        user=request.user
    ).select_related('product__category')
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})


def contacts_view(request):
    return render(request, 'shop/contacts.html')


def about_view(request):
    return render(request, 'shop/about.html')


def delivery_view(request):
    return render(request, 'shop/delivery.html')


@staff_member_required
def admin_dashboard(request):
    from accounts.models import CustomUser
    from orders.models import Order
    total_users = CustomUser.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_revenue = Order.objects.filter(
        status__in=['processing', 'shipped', 'delivered']
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    orders_by_status = {
        'pending': Order.objects.filter(status='pending').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created')[:10]
    recent_users = CustomUser.objects.order_by('-date_joined')[:10]

    top_products = Product.objects.annotate(
        sold=Count('order_items')
    ).order_by('-sold')[:5]

    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_month = CustomUser.objects.filter(date_joined__gte=thirty_days_ago).count()
    new_orders_month = Order.objects.filter(created__gte=thirty_days_ago).count()

    return render(request, 'shop/admin_dashboard.html', {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'orders_by_status': orders_by_status,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'top_products': top_products,
        'new_users_month': new_users_month,
        'new_orders_month': new_orders_month,
    })


@staff_member_required
def admin_orders(request):
    from orders.models import Order

    status_filter = request.GET.get('status', '')
    orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created')

    if status_filter:
        orders = orders.filter(status=status_filter)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        if order_id and new_status:
            Order.objects.filter(id=order_id).update(status=new_status)
            messages.success(request, f'Статус замовлення #{order_id} змінено.')
            return redirect('shop:admin_orders')

    return render(request, 'shop/admin_orders.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@staff_member_required
def admin_users(request):
    from accounts.models import CustomUser
    users = CustomUser.objects.order_by('-date_joined')
    return render(request, 'shop/admin_users.html', {'users': users})