from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q




def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)  

    
    try:
        cart_item = CartItem.objects.get(cart__cart_id=cart_id, product=product)
        cart_item.quantity += 1  
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart_id=cart_id
        )
    
    return redirect('store') 






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






def search(request):
    products = []
    products_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }   
    return render(request, 'store/store.html', context)







