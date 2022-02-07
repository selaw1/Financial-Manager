from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from moneyaccount.models import MoneyAccount


class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", 'password1', 'password2')

class MoneyAccountForm(forms.ModelForm):
    
    class Meta:
        model = MoneyAccount
        fields = ("name", "total_balance", "bank", "account_type", "is_main")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.user = user
        self.fields['is_main'].label = 'make main account'
        self.fields['total_balance'].widget.attrs['min'] = 0

    def clean(self):
        """Validate fields"""
        super().clean()

        initial_errors = self.errors.as_data()
        name = self.cleaned_data['name']

        if "is_main" not in initial_errors:
            is_main = self.cleaned_data['is_main']

            my_accounts = MoneyAccount.objects.filter(user=self.user)
            my_main_accounts = my_accounts.filter(is_main=True)
            same_name_accounts = my_accounts.filter(name__iexact=name)

            if 'create' in self.data:
                if is_main and my_main_accounts:
                    self.add_error("is_main", "Can't have more than 1 account as a main account")

                if name and same_name_accounts:
                    self.add_error('name', 'you already have an account with the same name.')


            if 'update' in self.data:
                if is_main and my_main_accounts.exclude(pk=self.instance.id):
                    self.add_error("is_main", "Can't have more than 1 account as a main account")

                if name and same_name_accounts.exclude(pk=self.instance.id):
                    self.add_error('name', 'you already have an account with the same name.')

