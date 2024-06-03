from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Person, Consumption


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'weight']
        labels = {
            'name': 'Nome',
            'weight': 'Peso'
        }


class ConsumptionForm(forms.ModelForm):
    AMOUNTS = [
        (250, 'Copo pequeno 250ml'),
        (350, 'Copo médio 350ml'),
        (500, 'Garrafa média 500ml'),
    ]

    amount = forms.ChoiceField(choices=AMOUNTS, widget=forms.RadioSelect)

    class Meta:
        model = Consumption
        fields = ['amount']
        labels = {
            'amount': 'Quantidades'
        }
