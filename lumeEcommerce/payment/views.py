from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem, User
from cart.cart import Cart
from django.http import JsonResponse
from django.conf import settings

def checkout(request):
    paypal_client_id = settings.PAYPAL_CLIENT_ID
    sellers = User.objects.filter(is_active=True)
    
    # Users with accounts - Pre-fill the form
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {
                'shipping': shipping_address,
                'paypal_client_id': paypal_client_id,
                'sellers': sellers
            }
            return render(request, 'payment/checkout.html', context=context)
        except ShippingAddress.DoesNotExist:
            # Authenticated users with no shipping information
            return render(request, 'payment/checkout.html', {
                'paypal_client_id': paypal_client_id
            })

    # Guest users
    return render(request, 'payment/checkout.html', {
        'paypal_client_id': paypal_client_id
    })


def payment_success(request):
    # Clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        zipcode = request.POST.get('zipcode')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        seller_id = request.POST.get('seller')
        payment_method = request.POST.get('payment_method')

        shipping_address = (address1 + "\n" + address2 +
                            "\n" + city + "\n" + state + "\n" + zipcode)

        # Shopping cart information
        cart = Cart(request)
        total_cost = cart.get_total()

        # Validate seller
        try:
            seller = User.objects.get(id=seller_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid seller selected'})

        # Validate payment method
        valid_payment_methods = [choice[0] for choice in Order.PAYMENT_METHODS]
        if payment_method not in valid_payment_methods:
            return JsonResponse({'success': False, 'error': 'Invalid payment method'})

        if request.user.is_authenticated:
            profile = request.user.profile

            discount = 0
            if profile.supports_flamengo:
                discount += 0.10
            if profile.watches_one_piece:
                discount += 0.05
            if profile.city and profile.city.strip().lower() == 'sousa':
                discount += 0.15

            discounted_total = total_cost - (total_cost * discount)

            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=discounted_total,
                payment_method=payment_method,
                user=request.user,
                seller=seller,
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user
                )

        else:
            # Guest user: no discount
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                payment_method=payment_method,
                user=None,
                seller=seller,
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=None
                )

        # Clear cart
        del request.session['session_key']

        return JsonResponse({'success': True})

