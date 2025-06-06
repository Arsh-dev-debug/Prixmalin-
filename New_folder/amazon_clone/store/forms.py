from django import forms
import re
from datetime import datetime
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'body']
        labels = {
            'body': 'Comment',
        }
        
class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Card details
    cc_name = forms.CharField(max_length=100, label="Name on card", widget=forms.TextInput(attrs={'class': 'form-control'}))
    cc_number = forms.CharField(max_length=16, label="Credit card number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    cc_expiration = forms.CharField(max_length=5, label="Expiration (MM/YY)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    cc_cvv = forms.CharField(max_length=4, label="CVV", widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not re.match(r'^\d{6}$', zip_code):
            raise forms.ValidationError("Invalid PIN code format. Please enter a 6-digit PIN code")
        return zip_code

    def clean_state(self):
        state = self.cleaned_data.get('state')
        indian_states = [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 
            'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 
            'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 
            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 
            'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 
            'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
            'Andaman and Nicobar Islands', 'Chandigarh', 
            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 
            'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 
            'Puducherry'
        ]
        
        if state not in indian_states:
            raise forms.ValidationError("Invalid state. Please use a valid Indian state name")
        return state
    
    def clean_cc_expiration(self):
        expiration = self.cleaned_data.get('cc_expiration')
        if not re.match(r'^(0[1-9]|1[0-2])\/([0-9]{2})$', expiration):
            raise forms.ValidationError("Invalid expiration format (use MM/YY)")

        try:
            month, year = map(int, expiration.split('/'))
            exp_date = datetime(2000 + year, month, 1)
            if exp_date <= datetime.now():
                raise forms.ValidationError("Card has expired")
        except:
            raise forms.ValidationError("Invalid expiration date")
            
        return expiration

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))