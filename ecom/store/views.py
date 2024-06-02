from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .forms import ChangePasswordForm, SignUpForm, UpdateUserForm
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

def update_user(request, user_id):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=user_id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Your Profile Has Been Updated Successfully.")
            return redirect("update_user", user_id)
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You Must Login First!")
        return redirect("home")
    
def update_password(request, user_id):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=user_id)
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password Has Been Updated Successfully. Please Login Again.")
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password", user_id)
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html",{"form": form})
    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")

def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Welcome To Our Online Shop. Please Enjoy Shopping With Us."))
            messages.success(request, ())
            return redirect("home")
        else:
            messages.success(request, ("Whoops, There Was A Problem Registering, Please Try Agian.."))
            return redirect("register")
    else:
        return render(request, "register.html", {
            "form": form
        })
    
def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product.html", {
        "product": product
    })

def category(request, foo):
    foo = foo.replace("-", " ")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, "category.html", {
            "category": category,
            "products": products
        })
    except:
        messages.success(request, ("Nothing Matches The Keyword.."))
        return redirect("home")
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {
        "categories": categories,
    })
