

# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, Order , CartItem
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already taken")
            return redirect("/register/")
        
        user = User.objects.create(username=username, email=email)

        user.set_password(password)
        user.save()

        messages.info(request, "Account created Successfully")

        return redirect('/register')
             
            
            
    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # if User.objects.filter(username = username).exists():
        #     messages.error(request, "Invalid Username")
        
        user = authenticate(request, username=username, password=password)

        if user is None:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Invalid Password")
            else:
                messages.error(request, "Invalid Username and Password ")
            return redirect("/login/")
        else:
            login(request, user)
            
            return redirect('/')
        
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")


@login_required
def home(request):
    trending_products = Product.objects.filter(is_trending=True)  # Get all trending products
    return render(request, 'shop/homepage.html', {'trending_products': trending_products})


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def place_order(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')

        if not shipping_address:
            # Handle the case where the address is not provided
            return render(request, 'shop/place_order.html', {
                'product': product,
                'error_message': "Shipping address is required."
            })
        
        total_price = float(request.POST.get('total_price'))  # This is the dynamically calculated total price
        order = Order(
            user=request.user,  # Associate the order with the logged-in user
            product=product,
            quantity=quantity,
            total_price=total_price,
            payment_method=payment_method,
            shipping_address=shipping_address
        )
        order.save()
        return redirect('order_success')

    return render(request, 'shop/place_order.html', {'product': product})

def order_success(request):
    return render(request, 'shop/order_success.html')


#Views for adding products through HTML form


# Custom test for superuser
def is_superuser(user):
    return user.is_superuser

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle both form data and file upload
        if form.is_valid():
            form.save()  # Save the new product to the database
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


#Views to see which orders are placed

@login_required
def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = [] 
    # orders = Order.objects.all()  # Get all orders from the database
    for order in orders:
        order.created_at = timezone.localtime(order.created_at)  # Convert to local time (IST)
    return render(request, 'shop/order_list.html', {'orders': orders})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Add or update the item in the cart
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f'{product.name} has been added to your cart.')
        return redirect('product_detail', product_id=product.id)  # Redirect back to the product detail page
    else:
        # Handle unauthenticated users (redirect to login, etc.)
        return redirect('login')  # Adjust as necessary
    

@login_required
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []  # Or handle unauthenticated users as needed
    return render(request, 'shop/cart.html', {'cart_items': cart_items})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('/cart/')

@staff_member_required
def all_orders(request):
    orders = Order.objects.all()  # Fetch all orders (you can filter as needed)
    return render(request, 'shop/AllOrder_list.html', {'orders': orders})