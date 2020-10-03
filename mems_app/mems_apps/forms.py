from django import forms
from .models import MessExtra, Order


class MessExtrasForm(forms.ModelForm):
    """"""

    class Meta:
        model = MessExtra
        fields = ['name', 'price', 'discription', 'quantity']


class OrderForm(forms.ModelForm):
    """"""

    class Meta:
        model = Order
        fields = ['extras_type', 'quantity']