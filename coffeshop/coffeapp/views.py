from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *



# def signin(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  
#             else:
#                 return render(request, 'sign_in_page.html', {'form': form})
#     elif request.method == 'GET':
#         form = LoginForm()
#         return render(request, 'sign_in_page.html', {'form': form})

def signin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('coffeapp:home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('coffeapp:home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'sign_in_page.html', context)


def logoutUser(request):
    logout(request)
    return redirect('coffeapp:home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('coffeapp:home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'sign_up_page.html', {'form': form})

# def newproductPage(request):
#     form = ProductsForm(request.POST)
#     if form.is_valid():


def home(request):
    products= Products.objects.all
    context= {'products': products}
    return render(request, 'home.html', context)

@login_required(login_url='coffeapp:signin')
def productsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products= Products.objects.filter(Q(vertical__icontains= q))
    product_types = Products.vertical
    product_prices= Products.price
    context= {'products': products, 'product_types': product_types, 'product_prices':product_prices}
    return render(request, 'products.html', context)

def createProduct(request):
    if request.user != User.is_superuser:
        return HttpResponse('You are not allowed here!!!!')

    form = ProductsForm()
    if request.method == 'POST':
        form= ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coffeapp:home')

    context={'form': form}
    return render(request, 'new_product.html', context)


def manageProduct(request):
    form =StorageForm(request.POST)
    storage = Storage.objects.first()  # assuming only one Storage object
    if request.method == 'POST':
        form = StorageForm(request.POST, instance=storage)
        if form.is_valid():
            form.save()
        return redirect('dashboard')
    else:
        form = StorageForm(instance=storage)



    context={'form': form}
    return render(request, 'manage-product.html', context)

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    form = AddToCartForm(request.POST or None)
    
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        # بررسی موجودی انبار
        ingredients = {
            'sugar': product.sugar * quantity,
            'coffee': product.coffee * quantity,
            'flour': product.flour * quantity,
            'chocolate': product.chocolate * quantity
        }
        
        for ingredient, amount in ingredients.items():
            storage = Storage.objects.get(name=ingredient)
            if storage.amount < amount:
                messages.error(request, f'موجودی {ingredient} کافی نیست.')
                return redirect('product_detail', product_id=product_id)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        messages.success(request, 'محصول به سبد خرید اضافه شد.')
        return redirect('view_cart')
    
    return render(request, 'add_to_cart.html', {'form': form, 'product': product})




@login_required
def checkout(request):
    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        
        # ایجاد سفارش
        order = Orders.objects.create(
            username=request.user.username,
            products=', '.join([item.product.name for item in items]),
            purchase_amount=sum(item.product.price * item.quantity for item in items),
            type=order_type
        )
        
        # کم کردن از موجودی انبار
        for item in items:
            product = item.product
            Storage.objects.filter(name='sugar').update(amount=F('amount') - product.sugar * item.quantity)
            Storage.objects.filter(name='coffee').update(amount=F('amount') - product.coffee * item.quantity)
            Storage.objects.filter(name='flour').update(amount=F('amount') - product.flour * item.quantity)
            Storage.objects.filter(name='chocolate').update(amount=F('amount') - product.chocolate * item.quantity)
        
        # پاک کردن سبد خرید
        cart.delete()
        
        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return redirect('order_confirmation')
    
    return redirect('view_cart')