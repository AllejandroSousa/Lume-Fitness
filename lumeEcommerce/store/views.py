from django.shortcuts import render, redirect
from .models import Category, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, CategoryForm

# Create your views here.

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_staff)
def admin_merchandise(request):
    # Pesquisa de produtos
    product_query = request.GET.get('product_search', '')
    if product_query:
        products = Product.objects.filter(title__icontains=product_query)
    else:
        products = Product.objects.all()

    # Pesquisa de categorias
    category_query = request.GET.get('category_search', '')
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

    context = {
        'products': products,
        'categories': categories,
        'product_form': product_form,
        'category_form': category_form,
        'product_query': product_query,  # Para manter o valor no campo de pesquisa
        'category_query': category_query,  # Para manter o valor no campo de pesquisa
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


def store(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'store/store.html', context)

def search_results(request):
    products = Product.objects.all()
    
    # Filtro por nome
    name_query = request.GET.get('name', '')
    if name_query:
        products = products.filter(title__icontains=name_query)
    
    # Filtro por faixa de preço
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Filtro por categoria
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category__id=category_id)
    
    # Filtro por produtos fabricados em Mari
    made_in_mari = request.GET.get('made_in_mari', '')
    if made_in_mari:
        products = products.filter(made_in_mari=True)
    
    # Filtro específico para funcionários (produtos com baixo estoque)
    if request.user.is_authenticated and request.user.is_staff:
        low_stock = request.GET.get('low_stock', '')
        if low_stock:
            products = products.filter(stock__lt=5)
    
    categories = Category.objects.all()
    context = {
        'all_products': products,
        'categories': categories,
        'name_query': name_query,
        'min_price': min_price,
        'max_price': max_price,
        'category_id': category_id,
        'made_in_mari': made_in_mari
    }
    
    return render(request, 'store/store_filter.html', context)


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

