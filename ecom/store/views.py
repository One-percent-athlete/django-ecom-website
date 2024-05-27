from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Customer, Category, Order

def home(request):
    products = Product.objects.all()

    return render(request, "home.html", {
        "products": products
    })

def about(request):
    return render(request, "about.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome Back, {username}")
            return redirect("home")
        else:
            messages.success(request, "Username Or Password Is Incorrect.")
            return redirect("login")
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("See You Again Soon..."))
    return redirect("home")