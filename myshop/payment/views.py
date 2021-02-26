from io import BytesIO

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import braintree
import weasyprint

from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # create invoice e-mail
            subject = 'jTro - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject, message, 'admin@jtro.com', ['khan.email'])

            # generate PDF
            html = render_to_string('orders/pdf.html', {'order': order})
            out = BytesIO()
            stylesheet = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheet=stylesheet)

            # attach pdf
            email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')

            # send e-mail
            email.send()
            return redirect('done')
        else:
            return redirect('canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        context = {
            'order': order,
            'client_token': client_token
        }
        return render(request, 'payment/process.html', context)


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


