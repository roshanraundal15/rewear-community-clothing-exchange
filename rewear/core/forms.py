from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'size',
            'condition',
            'tags',
            'type',
            'price',
            'image'
        ]

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get("type")
        price = cleaned_data.get("price")

        # For "sell" and "redeem", price must be a positive integer
        if item_type in ['sell', 'redeem']:
            if price is None or price <= 0:
                self.add_error('price', f"Price must be greater than 0 for '{item_type}' items.")
        else:
            # Clear price if type is 'swap'
            cleaned_data['price'] = None

        return cleaned_data


from .models import SwapRequest

class SwapRequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ['offered_item']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['offered_item'].queryset = Item.objects.filter(
            uploader=user, status='available', type='swap'
        )
        self.fields['offered_item'].label = "Select an item to offer in exchange"
