from django.shortcuts import render
from .forms import ShippingForm

# Create your views here.
def payment_success(request):

    

    return render(request, "payment/payment_success.html", {
    })