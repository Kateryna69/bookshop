from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import UserProfile
from orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.phone = form.cleaned_data.get('phone', '')
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.city = form.cleaned_data.get('city', '')
            profile.save()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.first_name or user.username}!')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Виправте помилки у формі.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Ласкаво просимо, {user.first_name or user.email}!')
                return redirect(request.GET.get('next', '/'))
        messages.error(request, 'Невірний email або пароль.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з акаунту.')
    return redirect('shop:product_list')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created')[:5]
    edit_mode = request.GET.get('edit') == '1'

    if request.method == 'POST':
        if 'delete_avatar' in request.POST:
            if request.user.avatar:
                request.user.avatar.delete(save=True)
            messages.success(request, 'Фото видалено.')
            return redirect('accounts:profile')

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.phone = form.cleaned_data.get('phone', '')
            if request.FILES.get('avatar'):
                if request.user.avatar:
                    request.user.avatar.delete(save=False)
                request.user.avatar = request.FILES['avatar']
            request.user.save()
            form.save()
            messages.success(request, '✅ Профіль успішно оновлено!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Виправте помилки у формі.')
            edit_mode = True
    else:
        form = ProfileForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone': getattr(request.user, 'phone', ''),
            }
        )

    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders,
        'edit_mode': edit_mode,
    })