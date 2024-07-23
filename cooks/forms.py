from django import forms
from .models import Booking, Single, TeamCook, Contact

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name', 'username', 'email', 'address', 'city', 'state',
            'zip_code', 'phone', 'cookTime', 'time', 'occasion', 
            'speciality', 'dish'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Cook Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter your state'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Enter your zip code'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'cookTime': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Select a time'}),
            'occasion': forms.TextInput(attrs={'placeholder': 'Enter the occasion'}),
            'speciality': forms.TextInput(attrs={'placeholder': 'Enter the speciality'}),
            'dish': forms.TextInput(attrs={'placeholder': 'Enter the dish'}),
        }

class SingleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Single
        fields = ['name','password','email', 'experience', 'speciality', 'dish', 'gender', 'desc', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter your Experience (in years)'}),
            'speciality': forms.TextInput(attrs={'placeholder': 'Enter the speciality'}),
            'dish': forms.TextInput(attrs={'placeholder': 'Enter the dish'}),
             'gender': forms.Select(choices=Single.GENDER_CHOICES, attrs={'placeholder': 'Select a gender'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Enter the extra details'}),
            'photo': forms.FileInput(),
        }

class TeamCookRegistrationForm(forms.ModelForm):
    class Meta:
        model = TeamCook
        fields = ['name', 'password', 'email', 'experience', 'teamName', 'people', 'speciality', 'dish', 'desc',  'photo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter your Experience (in years)'}),
            'teamName': forms.TextInput(attrs={'placeholder': 'Enter your Team Name'}),
            'people': forms.NumberInput(attrs={'placeholder': 'Enter Team Size'}),
            'speciality': forms.TextInput(attrs={'placeholder': 'Enter the speciality'}),
            'dish': forms.TextInput(attrs={'placeholder': 'Enter the dish'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Enter the extra details'}),
            'photo': forms.FileInput(),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email','subject','message']
class PaymentForm(forms.Form):
    name = forms.CharField(max_length=255, label="Name on Card")
    card_number = forms.CharField(max_length=16, label="Card Number")
    exp_month = forms.IntegerField(min_value=1, max_value=12, label="Expiration Month (MM)")
    exp_year = forms.IntegerField(min_value=2023, max_value=2100, label="Expiration Year (YYYY)")
    cvv = forms.CharField(max_length=4, label="CVV")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
