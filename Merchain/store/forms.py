from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Bid, Product
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.use_custom_control = True

    name = forms.CharField(required=False)
    price = forms.FloatField(required=False)
    description = forms.TextInput()
    image = forms.ImageField(required=False)


    class Meta:
        model = Product
        fields = ['name', 'price', 'deadline', 'description', 'image']
        widgets = {
            'deadline': DateTimeInput(),
            'description': forms.Textarea(attrs={'rows': 5})
        }

    def clean_content(self):
        price = self.cleaned_data.get('price')

        if float(price) < 0:
            raise ValidationError("Negative price!")

        return price

class BidForm(ModelForm):

    class Meta:
        model = Bid
        fields = ['amount']

        