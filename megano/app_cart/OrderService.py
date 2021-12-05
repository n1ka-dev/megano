from app_cart.models import DeliveryMethod, PaymentMethod
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
    def __init__(self, request):
        self.session = request.session
        order = self.session.get(settings.ORDER_SESSION_ID)
        if not order:
            # save an empty cart in the session
            order = self.session[settings.ORDER_SESSION_ID] = {}
        self.order = order
        self.display_names = {}

    def save(self, data):
        """ Обновление сессии """
        self.order = self.session[settings.ORDER_SESSION_ID] = data
        code = self.order['s-row']['delivery_method']
        d_name = DeliveryMethod.objects.get(code=code).display_name
        self.display_names[code] = d_name

        code_payment = self.order['s-row']['payment_method']
        p_name = PaymentMethod.objects.get(code=code_payment).display_name
        self.display_names[code_payment] = p_name
        self.session.modified = True

    def get_html(self):
        out_list = []
        print(self.order.items())
        for i, row in self.order.items():
            out_list.append('<div class="row-block">')
            for name, val in row.items():
                if val in self.display_names:
                    val = self.display_names[val]
                out_list.extend(['<div class="Order-info"><div class="Order-infoType">', dict_order_names[name],
                                 ' : </div><div class="Order-infoContent">', val, '</div></div>'])
            out_list.append('</div>')
        return ' '.join(out_list)
