from django.shortcuts import render
from store.models import Seller
from .models import ShippingAddress, Order, OrderItem, User
from cart.cart import Cart
from django.http import JsonResponse
from django.conf import settings

def checkout(request):
    paypal_client_id = settings.PAYPAL_CLIENT_ID
    sellers = Seller.objects.all()
    print(list(sellers))

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
                'paypal_client_id': paypal_client_id,
                'sellers': sellers
            })

    # Guest users
    return render(request, 'payment/checkout.html', {
        'paypal_client_id': paypal_client_id,
        'sellers': sellers
    })


def payment_success(request):
    # Clear shopping cart
    for key in list(request.session.keys()):
        if key == 'cart_key':
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

        seller = Seller.objects.get(id=seller_id)

        if request.user.is_authenticated:
            profile = request.user.customer_profile

            discount = 0
            if profile.has_discount():
                discount += 0.10
            print(total_cost, discount)
            discounted_total = float(total_cost) - (float(total_cost) * discount)

            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=discounted_total,
                payment_method=payment_method,
                customer=request.user,
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

                # Update product stock
                product = item['product']
                product.stock -= item['qty']
                product.save()

        else:
            # Guest user: no discount
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                payment_method=payment_method,
                customer=None,
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

                # Update product stock
                product = item['product']
                product.stock -= item['qty']
                product.save()

        return JsonResponse({'success': True})

