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

    def save(self, data):
        """ Обновление сессии """
        self.session[settings.ORDER_SESSION_ID] = data
        self.session.modified = True

    def get_html(self):
        out_list = []

        for i, row in self.order.items():
            out_list.append('<div class="row-block">')
            for name, val in row.items():
                print(name, val,'html')
                out_list.extend(['<div class="Order-info"><div class="Order-infoType">', dict_order_names[name],
                                ' : </div><div class="Order-infoContent">', val, '</div></div>'])
            out_list.append('</div>')
        return ' '.join(out_list)
