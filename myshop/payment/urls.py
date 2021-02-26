from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import (
    payment_process,
    payment_done,
    payment_canceled,
)


urlpatterns = [
    path(_('process/'), payment_process, name='process'),
    path(_('done/'), payment_done, name='done'),
    path(_('canceled/'), payment_canceled, name='canceled'),
]
