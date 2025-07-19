"""Form definitions for the shop application."""
from django import forms
"""Form for handling shop-related user input."""
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")
