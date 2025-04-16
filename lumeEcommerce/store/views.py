from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.urls import reverse
from payment.models import Order
from .models import Category, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, CategoryForm, ProductFilterForm

# Create your views here.

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def admin_merchandise(request):
    # Lógica existente para produtos e categorias
    # Lógica existente para produtos e categorias
    product_query = request.GET.get('product_search', '')
    if product_query:
        products = Product.objects.filter(title__icontains=product_query)
    else:
        products = Product.objects.all()

    # Pesquisa de categorias
    category_query = request.GET.get('category_search', '')
    products = Product.objects.all()  # Ajuste conforme seu modelo
    categories = Category.objects.all()  # Ajuste conforme seu modelo
    product_form = ProductForm()  # Ajuste conforme seu formulário
    category_form = CategoryForm()  # Ajuste conforme seu formulário

    if product_query:
        products = products.filter(title__icontains=product_query)
    if category_query:
        categories = Category.objects.filter(name__icontains=category_query)
    else:
        categories = Category.objects.all()

    # Formulário para adicionar produto
    product_form = ProductForm()
    if request.method == 'POST' and 'add_product' in request.POST:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('admin_merchandise')

    # Formulário para adicionar categoria
    category_form = CategoryForm()
    if request.method == 'POST' and 'add_category' in request.POST:
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('admin_merchandise')

    # Lógica para gerenciar pedidos
    orders = Order.objects.filter(order_status='Pendent')
    if request.method == 'POST' and 'order_id' in request.POST:
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        try:
            order = Order.objects.get(id=order_id)
            if action == 'approve':
                order.order_status = 'Confirmed'
            elif action == 'reject':
                order.order_status = 'Rejected'
            order.save()
        except Order.DoesNotExist:
            pass

        base_url = reverse('admin_merchandise')
        query_string = urlencode({'tab': 'manage-orders'})
        url = f'{base_url}?{query_string}'
        return redirect(url)

    # Lógica para relatório de vendas (somente superuser)
    sales_by_seller = {}
    total_sales = 0
    if request.user.is_superuser:
        confirmed_orders = Order.objects.filter(order_status='Confirmed')
        for order in confirmed_orders:
            seller = order.seller
            if seller not in sales_by_seller:
                sales_by_seller[seller] = 0
            sales_by_seller[seller] += order.amount_paid
            total_sales += order.amount_paid

    context = {
        'products': products,
        'product_query': product_query,
        'categories': categories,
        'category_query': category_query,
        'product_form': product_form,
        'category_form': category_form,
        'orders': orders,
        'sales_by_seller': sales_by_seller,
        'total_sales': total_sales,
    }

    return render(request, 'store/admin_merchandise.html', context)

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_merchandise')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/admin_management/edit_product.html', {'form': form, 'product': product})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_merchandise')
    return render(request, 'store/admin_management/delete_product.html', {'product': product})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_merchandise')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/admin_management/edit_category.html', {'form': form, 'category': category})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_merchandise')
    return render(request, 'store/admin_management/delete_category.html', {'category': category})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def manage_orders(request):
    orders = Order.objects.filter(status='Pending')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')  # 'approve' ou 'reject'

        try:
            order = Order.objects.get(id=order_id)
            if action == 'approve':
                order.order_status = 'Confirmed'
            elif action == 'reject':
                order.order_status = 'Rejected'
            order.save()
        except Order.DoesNotExist:
            pass

        return redirect('manage_orders')
        

    return render(request, 'store/admin_merchandise.html', {'orders': orders})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('store')

    confirmed_orders = Order.objects.filter(status='Confirmed')

    sales_by_seller = {}
    total_sales = 0
    for order in confirmed_orders:
        seller = order.seller
        if seller not in sales_by_seller:
            sales_by_seller[seller] = 0
        sales_by_seller[seller] += order.total
        total_sales += order.total

    return render(request, 'store/admin_merchandise.html', {
        'sales_by_seller': sales_by_seller,
        'total_sales': total_sales
    })


def store(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'store/store.html', context)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', {'category': category, 'products': products})

def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product-info.html', context)

def product_list(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    is_made_in_mari = request.GET.get('is_made_in_mari')

    products = Product.objects.all()

    if category:
        products = products.filter(category__name=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if is_made_in_mari is not None and is_made_in_mari != '':
        products = products.filter(is_made_in_mari=is_made_in_mari)

    context = {
        'products': products,
        'filter_form': ProductFilterForm(request.GET)
    }
    return render(request, 'store/product_list.html', context)


