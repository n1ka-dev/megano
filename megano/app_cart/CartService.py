from app_cart.models import Orders
from app_shop.models import Product
from megano import settings


class CartService:
    def __init__(self, request, init_id_cart=False):
        self.session = request.session

        if init_id_cart and Orders.objects.filter(uid=init_id_cart).exists():
            self.id_cart = str(init_id_cart)
        else:
            self.id_cart = settings.CART_SESSION_ID

        cart = self.session.get(self.id_cart)

        if not cart:
            if self.id_cart == settings.CART_SESSION_ID:
                cart = {}
            else:
                cart = {str(order_rec.product.id): {'quantity': order_rec.count, 'price': float(order_rec.price)}
                        for order_rec in Orders.objects.get(uid=self.id_cart).orderrecord_set.all()}

        self.session[self.id_cart] = self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for pr in products:
            product = {'id': pr.id, 'name': pr.name, 'price': float(pr.price), 'slug': pr.slug,
                       'images': [{'url': im.image.url, 'alt': im.alt} for im in pr.images.all()]}

            self.cart[str(product['id'])]['product'] = product

        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, count=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': float(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = int(count)
        else:
            self.cart[product_id]['quantity'] += int(count)

        self.save()

    def save(self):
        """ Обновление сессии cart """
        self.session[self.id_cart] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """ удаление корзины из сессии """
        del self.session[self.id_cart]
        self.session.modified = True

    def get_sum(self):
        return sum(float(item['price']) * item['quantity'] for item in
                   self.cart.values()) if self.cart else 0.0

    def get_count(self):
        return len(self.cart) if self.cart else 0
