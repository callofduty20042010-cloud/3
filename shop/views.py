from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.db.models import Q


# Create your views here.


@login_required(login_url='/users/sign_in')
def product_list(request):
    search = request.GET.get('search')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    products = Product.objects.all()
    slides = Slide.objects.all
    product_id = request.GET.get('product')
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        cart_item = CartItem.objects.filter(product=product, customer=request.user)
        if not cart_item:
            CartItem.objects.create(customer=request.user, product=product, quantity=1)
            return redirect('shop:product_list')
        for item in cart_item:
            item.quantity += 1
            item.save()
    products = Product.objects.filter(category=category) if category else products
    products = Product.objects.filter(brand=brand) if brand else products
    products = Product.objects.filter(Q(title__icontains=search) |
                                      Q(description__icontains=search)) if search else products
    return render(request, 'product_list.html', {
        'products':products,
        'slides': slides
    })

def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render( request, 'cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price
    })


def delete_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk).delete()
    return redirect('shop:cart')


def edit_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    action = request.GET.get('action')

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('shop:cart')
        cart_item.quantity -=1
        cart_item.save()
        return redirect('shop:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop:cart')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {
        'product':product
    })


def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)    
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])

    form = OrderForm()
    if not cart_items:
        return redirect('shop:cart')
    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price = total_price
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()
        return redirect('shop:cart')
    return render(request, 'create_order.html', {
        'total_price': total_price,
        'amount': amount,
        'cart_items': cart_items,
        'form': form
    })

