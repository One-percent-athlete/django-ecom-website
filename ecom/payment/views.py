from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User

from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import PaymentForm, ShippingForm
from cart.cart import Cart
from store.models import Product

# Create your views here.
def payment_success(request):

    return render(request, "payment/payment_success.html", {
    })

def checkout(request):
    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, "payment/checkout.html", {"products": products,
        "quantities": quantities,
        "totals":totals,
        "shipping_form": shipping_form,
        })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"products": products,
        "quantities": quantities,
        "totals":totals,
        "shipping_form": shipping_form,                        
        })

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.cart_total()
        billing_form = PaymentForm()

        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping

        if request.user.is_authenticated:
             return render(request, "payment/billing_info.html", {"products": products,
        "quantities": quantities,
        "totals":totals,
        "shipping_info": request.POST,
        "billing_form":billing_form
        })
        else:
            return render(request, "payment/billing_info.html", {"products": products,
        "quantities": quantities,
        "totals":totals,
        "shipping_info": request.POST,
        "billing_form":billing_form
        })

    else:
        messages.success(request, "Access Denied...")
        return redirect("home")


def process_order(request):
    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        cart = Cart(request)
        products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()

        my_shipping = request.session.get("my_shipping")
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}"

        if request.user.is_authenticated:
            user = request.user

            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=totals)
            create_order.save()

            order_id = create_order.pk

            for product in products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()


            messages.success(request, "Order Placed...")
            return render(request, "payment/process_order.html", {})
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=totals)
            create_order.save()

            order_id = create_order.pk

            for product in products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            messages.success(request, "Order Placed...")
            return render(request, "payment/process_order.html", {})

        
        
    else:  
        messages.success(request, "Access Denied...")
        return redirect("home")
        

