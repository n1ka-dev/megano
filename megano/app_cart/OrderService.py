from app_cart.models import DeliveryMethod, PaymentMethod, Orders
from app_shop.models import Product
from megano import settings

dict_order_names = {
    'fio': 'ФИО',
    'phone': 'Телефон',
    'email': 'E-mail',
    'delivery_method': 'Тип доставки',
    'city': 'Город',
    'address': 'Адрес',
    'payment_method': 'Оплата',
}


class OrderService:
    def __init__(self, request, init_id_cart=False):
        self.code_payment = None
        self.session = request.session
        order = self.session.get(settings.ORDER_SESSION_ID, {})

        self.delivery_method = ''
        self.order = order
        self.display_names = {}

        if init_id_cart:
            order_exist = Orders.objects.filter(uid=init_id_cart).exists()
            if order_exist:
                self.delivery_method = Orders.objects.get(uid=init_id_cart).delivery_method




    def save(self, data):
        """ Обновление сессии """
        self.order = self.session[settings.ORDER_SESSION_ID] = data
        code = self.order['s-row']['delivery_method']
        self.delivery_method = DeliveryMethod.objects.get(code=code)
        self.display_names[code] = self.delivery_method.display_name

        code_payment = self.order['s-row']['payment_method']
        pm_name = PaymentMethod.objects.get(code=code_payment).display_name
        self.display_names[code_payment] = pm_name
        self.code_payment = code_payment

        self.session.modified = True

    def get_delivery_price(self):
        return self.delivery_method.price if self.delivery_method else 0

    def get_html(self):
        out_list = []
        for i, row in self.order.items():
            out_list.append('<div class="row-block">')
            for name, val in row.items():
                if val in self.display_names:
                    val = self.display_names[val]
                out_list.extend(['<div class="Order-info"><div class="Order-infoType">', dict_order_names[name],
                                 ' : </div><div class="Order-infoContent">', val, '</div></div>'])
            out_list.append('</div>')
        return ' '.join(out_list)
