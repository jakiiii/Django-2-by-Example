from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    # Task to send an e-mail notification when an order is successfully created
    order = Order.objects.get(id=order_id)
    subject = 'Order no {}'.format(order.id)
    message = 'Dead {},\n\nYou have successfully placed an order.\nYour order id is {}.'.format(order.last_name, order.id)
    mail_sent = send_mail(subject, message, 'jaki@jtro.com', ['order.email.com'])
    return mail_sent
