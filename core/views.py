from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal
import json

from .models import Category, Meal, Cart, Order, OrderItem


def landing(request):
    if request.user.is_authenticated:
        return redirect('menu')
    categories = Category.objects.prefetch_related('meals').all()
    return render(request, 'core/landing.html', {'categories': categories})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif len(password) < 4:
            messages.error(request, 'Password must be at least 4 characters.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome to Abuja Flavours, {username}!')
            return redirect('menu')
    return render(request, 'core/auth.html', {'mode': 'signup'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'menu')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/auth.html', {'mode': 'login'})


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def menu_view(request):
    categories = Category.objects.prefetch_related('meals').all()
    active_category = request.GET.get('category', '')
    if active_category:
        meals = Meal.objects.filter(category__slug=active_category, is_available=True)
    else:
        meals = Meal.objects.filter(is_available=True)
    
    cart_items = Cart.objects.filter(user=request.user).values_list('meal_id', 'quantity')
    cart_dict = {meal_id: qty for meal_id, qty in cart_items}
    
    return render(request, 'core/menu.html', {
        'categories': categories,
        'meals': meals,
        'active_category': active_category,
        'cart_dict': cart_dict,
    })


@login_required
@require_POST
def add_to_cart(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, meal=meal,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    cart_count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({
        'success': True,
        'message': f'{meal.name} added to cart!',
        'cart_count': cart_count,
        'quantity': cart_item.quantity,
    })


@login_required
@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return JsonResponse({'success': True, 'removed': True, 'cart_count': Cart.objects.filter(user=request.user).count()})
    elif action == 'remove':
        cart_item.delete()
        return JsonResponse({'success': True, 'removed': True, 'cart_count': Cart.objects.filter(user=request.user).count()})
    
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'subtotal': float(cart_item.subtotal),
        'cart_count': Cart.objects.filter(user=request.user).count(),
    })


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('meal', 'meal__category')
    gross_total = sum(item.subtotal for item in cart_items)
    tax = gross_total * Decimal('0.15')
    net_total = gross_total + tax
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'gross_total': gross_total,
        'tax': tax,
        'net_total': net_total,
    })


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('meal')
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu')
    
    gross_total = sum(item.subtotal for item in cart_items)
    tax = gross_total * Decimal('0.15')
    net_total = gross_total + tax
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        payment_ref = request.POST.get('payment_reference', '').strip()
        
        if payment_method not in ['ecocash', 'card']:
            messages.error(request, 'Please select a valid payment method.')
            return render(request, 'core/checkout.html', {
                'cart_items': cart_items,
                'gross_total': gross_total,
                'tax': tax,
                'net_total': net_total,
            })
        
        if not payment_ref:
            messages.error(request, 'Please enter your payment details.')
            return render(request, 'core/checkout.html', {
                'cart_items': cart_items,
                'gross_total': gross_total,
                'tax': tax,
                'net_total': net_total,
            })
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                payment_reference=payment_ref,
                gross_total=gross_total,
                tax=tax,
                net_total=net_total,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    meal=item.meal,
                    meal_name=item.meal.name,
                    price=item.meal.price,
                    quantity=item.quantity,
                )
            cart_items.delete()
        
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'core/checkout.html', {
        'cart_items': cart_items,
        'gross_total': gross_total,
        'tax': tax,
        'net_total': net_total,
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/confirmation.html', {'order': order})
