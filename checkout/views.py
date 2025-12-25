from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from cart.models import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem, ShippingAddress


@login_required
def checkout(request):
    """
    Страница оформления заказа
    """
    cart = get_object_or_404(Cart, user=request.user)
    form = OrderCreateForm()

    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def thank_you(request, order_id):
    """
    Страница благодарности
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/thank_you.html', {'order': order})


@login_required
def create_order(request):
    """
    Создание заказа + отправка email админу
    """
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('store:home')

    if request.method != 'POST':
        return redirect('checkout:checkout')

    form = OrderCreateForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Ошибка в форме')
        return redirect('checkout:checkout')

    # --- создаём заказ ---
    order = Order.objects.create(
        user=request.user,
        payment_method=form.cleaned_data['payment_method'],
    )

    # --- адрес доставки ---
    shipping = ShippingAddress.objects.create(
        order=order,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
        phone=form.cleaned_data['phone'],
        address_line_1=form.cleaned_data['address_line_1'],
        address_line_2=form.cleaned_data['address_line_2'],
    )

    # --- товары ---
    items_lines = []
    total_price = 0

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity,
            price=cart_item.item.price,
        )

        line_total = cart_item.quantity * cart_item.item.price
        total_price += line_total

        items_lines.append(
            f"{cart_item.item.title} — {cart_item.quantity} шт. × {cart_item.item.price} ₽"
        )

    # --- email ---
    subject = f'Новый заказ №{order.id}'
    message = (
        f"Новый заказ\n\n"
        f"Покупатель: {shipping.first_name} {shipping.last_name}\n"
        f"Email: {shipping.email}\n"
        f"Телефон: {shipping.phone}\n\n"
        f"Адрес доставки:\n"
        f"{shipping.address_line_1}\n"
        f"{shipping.address_line_2 or ''}\n\n"
        f"Товары:\n"
        + "\n".join(items_lines) +
        f"\n\nИтого: {total_price} ₽"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    # --- очищаем корзину ---
    cart.clear()

    return redirect('checkout:thank_you', order_id=order.id)
