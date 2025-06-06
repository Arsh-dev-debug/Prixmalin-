from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import Product, Review, Cart, Order, OrderItem
from .forms import ReviewForm, CheckoutForm, ContactForm

def landing(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    return render(request, 'store/landing.html')

def home(request):
    products = Product.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).order_by('-release_date')
    
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-release_date', '-release_time')
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = f"{request.user.first_name} {request.user.last_name}"
            review.release_date = timezone.now().date()
            review.release_time = timezone.now().time()
            review.save()
            messages.success(request, 'Review added successfully!')
        else:
            messages.error(request, 'Error in form submission')
            
    return redirect('store:product_detail', product_id=product_id)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(manufacturer__icontains=query) | 
        Q(description__icontains=query)
    ).annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).order_by('-release_date')
    
    return render(request, 'store/home.html', {'products': products, 'search_query': query})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if item is already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    # If not created, it already exists so update quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Added to cart!')
    
    # Handle buy now functionality
    if request.method == 'POST' and request.POST.get('buy_now'):
        # Remove all other items from cart
        Cart.objects.filter(user=request.user).exclude(product=product).delete()
        return redirect('store:checkout')
        
    return redirect('store:product_detail', product_id=product_id)

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

from django.shortcuts import render

@login_required
def checkout(request):
    cart_items = []  # Your logic to fetch cart items
    total = 0        # Your total calculation
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('store:cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty')
        return redirect('store:cart')
        
    total = sum(item.product.price * item.quantity for item in cart_items)
    form = CheckoutForm()
    
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'form': form
    })

@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('store:checkout')
        
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty')
        return redirect('store:cart')
    
    form = CheckoutForm(request.POST)
    if form.is_valid():
        # Calculate total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Format shipping address
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zip_code = form.cleaned_data['zip_code']
        shipping_address = f"{address}, {city}, {state}, {zip_code}"
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            status='On its way'
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_time=item.product.price
            )
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('store:orders')
    else:
        messages.error(request, 'Please correct the errors in the form.')
        return redirect('store:checkout')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).annotate(
        item_count=Count('items')
    ).order_by('-order_date')
    
    return render(request, 'store/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all().select_related('product')
    
    return render(request, 'store/order_detail.html', {'order': order, 'items': items})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real application, you would handle the form data here
            # For now, just display a success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('store:contact')
    else:
        form = ContactForm()
        
    return render(request, 'store/contact.html', {'form': form})