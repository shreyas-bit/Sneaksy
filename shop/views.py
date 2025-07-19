# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Cart, Wishlist, CartItem , Order,OrderItem
from .forms import CheckoutForm


def home(request):
    """Display all available products on the home page."""
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def admin_login(request):
    return redirect('/admin/')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/products.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    """Handle user login with Django's AuthenticationForm."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def logout_view(request):
    """Log out the current user and redirect to the home page."""
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get the size from the POST data
    size = request.POST.get('size')
    if not size:
        # Handle missing size with a default or an error message
        return redirect('product_detail', product_id=product_id)  # or provide a default size

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create or update the CartItem with a specified size
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size  # Ensure size is passed here
    )

    if not item_created:
        # If the item already exists, increase the quantity
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    return redirect('view_cart')
def cart(request):
    if request.user.is_authenticated:
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
     
        cart_items = CartItem.objects.filter(cart=cart)

        
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return render(request, 'shop/cart.html', {
            'items': cart_items,
            'total_price': total_price
        })
    else:
        return redirect('login')
@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.products.all()  
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    """Add a product to the user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        messages.info(request, f"{product.name} is already in your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"Added {product.name} to your wishlist.")
    return redirect('wishlist')

@login_required
def remove_from_cart(request, product_id):
    # Retrieve the user's cart
    cart = Cart.objects.get(user=request.user)
    
    # Retrieve the 'size' parameter from the request
    size = request.GET.get('size')
    if not size:
        # Redirect to cart if size is not specified
        return redirect('cart')

    # Find the specific CartItem by cart, product, and size
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id, size=size)

    # If the quantity is greater than 1, decrement the quantity
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # If quantity is 1 or less, remove the cart item entirely
        cart_item.delete()

    return redirect('cart')
   
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product) 
    return redirect('wishlist')  

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def update_cart(request, item_id, quantity):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('view_cart')  

@login_required
def view_cart(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get all items in the cart
    items = CartItem.objects.filter(cart=cart)
    
    # Calculate the total price
    total_price = sum(item.product.price * item.quantity for item in items)
    
    return render(request, 'shop/cart.html', {
        'items': items,
        'total_price': total_price
    })
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category.html', {'category': category, 'products': products})
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    form = CheckoutForm()
    total_price = cart.get_total_price()  # Calculate total price of items in the cart

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                status="Deliverd"
            )

            # Create Order Items from Cart Items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart after successful checkout
            cart.items.all().delete()
            return redirect('order_history')  # Redirect to the order history page

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

