import datetime
from django import forms

from moneyaccount.models import Transaction


class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ("title", "note", "amount", "date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields['amount'].widget.attrs['min'] = 0
        self.fields['date'].initial = datetime.datetime.today()
        today = datetime.datetime.today()
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'value':today})
