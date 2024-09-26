from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug: 
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
    product_count = products.count()
    
    paginator = Paginator(products, 3)  
    page_number = request.GET.get('page')
    try:
        paged_products = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        paged_products = paginator.page(1)

    context = {
        'products': paged_products,
        'product_count': product_count,
        'links': Category.objects.all(),
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)





