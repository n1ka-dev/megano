from time import sleep

from app_cart.models import Orders
from megano.celery import app


@app.task()
def pay_service_emulation(cart_number, uid):
    print(cart_number, uid)
    print('pay_service_emulation')
    print(Orders.PAYMENT_ERROR)
    sleep(10)
    # если введённый номер чётный и не заканчивается на ноль,
    # то оплата подтверждается,
    # если введённый номер Нечётный или заканчивается на ноль,
    # то сервис генерирует случайную ошибку оплаты.

    order = Orders.objects.get(uid=uid)
    if cart_number % 2 == 0 and str(cart_number)[-1] != '0':
        status = Orders.PAID
    else:
        status = Orders.PAYMENT_ERROR

    # new = order.update(status=status)
    order.status = status
    order.save()
    print('status updated', uid, status)
