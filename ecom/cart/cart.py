
from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get("session_key")

        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if key == product.id:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def db_add(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_item = str(self.cart)
            cart_item = cart_item.replace("\'", "\"")
            current_user.update(old_cart=cart_item)


    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_item = str(self.cart)
            cart_item = cart_item.replace("\'", "\"")
            current_user.update(old_cart=cart_item)

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)

        cart = self.cart
        cart[product_id] = product_quantity

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_item = str(self.cart)
            cart_item = cart_item.replace("\'", "\"")
            current_user.update(old_cart=cart_item)

        new_cart = self.cart
        return new_cart
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_item = str(self.cart)
            cart_item = cart_item.replace("\'", "\"")
            current_user.update(old_cart=cart_item)