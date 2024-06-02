from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product


def cart_summary(request):
    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quantities

    totals = cart.cart_total()
    return render(request, "cart_summary.html",{"products": products,
     "quantities": quantities,
     "totals":totals                                         
    })

def cart_add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))


        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_quantity)

        qty = cart.__len__()

        response = JsonResponse({
            "qty": qty
            })
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        cart.update(product=product_id, quantity=product_quantity)

        response = JsonResponse({"qty": product_quantity})
        return response
        # return redirect("cart_summary")
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        
        cart.delete(product=product_id)

        response = JsonResponse({"product": product_id})
        return response