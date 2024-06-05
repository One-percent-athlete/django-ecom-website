from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
import json

from .forms import ChangePasswordForm, SignUpForm, UpdateUserForm, UserProfileForm
from payment.forms import ShippingForm
from .models import Product, Category, Profile
from payment.models import ShippingAddress
from cart.cart import Cart

def home(request):
    products = Product.objects.all()

    return render(request, "home.html", {
        "products": products
    })

def about(request):
    return render(request, "about.html", {})

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not products:
            messages.success(request, "The Product Doesn't Exist, Please Try Again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html",{
            "searched": searched,
            "products":products
            })
    else:
        return render(request, "search.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)

                cart = Cart(request)

                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


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
    
def update_profile(request, user_id):
    if request.user.is_authenticated:

        current_user = Profile.objects.get(user__id=user_id)
        form = UserProfileForm(request.POST or None, instance=current_user)

        shipping_user = ShippingAddress.objects.get(user__id=user_id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():

            form.save()

            shipping_form.save()
            messages.success(request, "Your Profile Has Been Updated Successfully.")
            return redirect("update_user", user_id)
        return render(request, "update_profile.html", {"form": form, "shipping_form": shipping_form})
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
            messages.success(request, ("Welcome To Our Online Shop. Please Fill Out Your Profile."))
            return redirect("update_profile", user.pk)
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
