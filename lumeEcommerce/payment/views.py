from django.shortcuts import render

from .models import ShippingAddress, Order, OrderItem, Seller, PaymentMethod
from cart.cart import Cart
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def seller_monthly_report(request):
    # Define o período (mês atual)
    today = timezone.now()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    
    first_day = timezone.datetime(year=year, month=month, day=1)
    if month == 12:
        last_day = timezone.datetime(year=year+1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = timezone.datetime(year=year, month=month+1, day=1) - timedelta(days=1)
    
    # Consulta dados de vendas por vendedor
    seller_stats = Order.objects.filter(
        date_ordered__gte=first_day,
        date_ordered__lte=last_day
    ).values(
        'seller__user__first_name',
        'seller__user__last_name'
    ).annotate(
        orders_count=Count('id'),
        total_sold=Sum('amount_paid')
    ).order_by('-total_sold')
    
    context = {
        'seller_stats': seller_stats,
        'month': month,
        'year': year,
        'month_name': first_day.strftime('%B')
    }
    
    return render(request, 'payment/seller_report.html', context)


def checkout(request):
    paypal_client_id = settings.PAYPAL_CLIENT_ID

    # Users with accounts - Pre-fill the form
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {
                'shipping': shipping_address,
                'paypal_client_id': paypal_client_id
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

        shipping_address = (address1 + "\n" + address2 +
                            "\n" + city + "\n" + state + "\n" + zipcode)

        # Shopping cart information
        cart = Cart(request)

        # Verificar estoque de todos os itens antes de processar a compra
        all_items_available = True
        for item in cart:
            product = item['product']
            quantity = item['qty']
            
            if product.stock < quantity:
                all_items_available = False
                break
        
        if not all_items_available:
            return JsonResponse({'success': False, 'error': 'Estoque insuficiente'})
        
        # Calcular desconto se o usuário estiver autenticado
        discount_percentage = 0
        total_cost = cart.get_total()
        discount_amount = 0
        
        if request.user.is_authenticated:
            try:
                profile = request.objects.get(user=request.user)
                discount_percentage = profile.discount_eligibility
                discount_amount = (discount_percentage / 100) * total_cost
                total_cost = total_cost - discount_amount
            except:
                pass
        
        # Criar forma de pagamento
        payment_method = PaymentMethod.objects.create(
            type=request.POST.get('payment_type', 'credit'),
            status='confirmed' if request.POST.get('payment_type') != 'boleto' else 'pending'
        )
        
        # Obter vendedor aleatório (ou específico baseado em alguma lógica)
        seller = None
        if Seller.objects.exists():
            seller = Seller.objects.order_by('?').first()
        
        # Criar ordem
        order = Order.objects.create(
            full_name=name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=total_cost,
            discount_amount=discount_amount,
            user=request.user if request.user.is_authenticated else None,
            seller=seller,
            payment_method=payment_method
        )
        
        order_id = order.pk
        
        # Criar itens de ordem e atualizar estoque
        for item in cart:
            product = item['product']
            quantity = item['qty']
            
            # Atualizar estoque
            product.stock -= quantity
            product.save()
            
            OrderItem.objects.create(
                order_id=order_id,
                product=product,
                quantity=quantity,
                price=item['price'],
                user=request.user if request.user.is_authenticated else None
            )
        
        order_success = True
        response = JsonResponse({'success': order_success})
        
        return response
