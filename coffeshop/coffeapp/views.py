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

