from django import forms
from .models import Order
from .bulma_mixin import BulmaMixin


class OrderForm(forms.Form, BulmaMixin):
    address = forms.CharField(label='Write your Address')
    phone = forms.CharField(label='Write your Phone')

    class Meta:
        model = Order
        fields = ('address', 'phone')