import random
import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from django.conf import settings
from django.urls import reverse

def defaultname():
    names = ["Cool Account", "Smile", "Blank", "Give Me a Name", "Unknown", "Anonymous"]
    return random.choice(names)

def make_uuid():
    return uuid.uuid4()

class AccountTypes(models.TextChoices):
    """Enumeration for the types of questions"""

    PERSONAL = "personal", "Personal" 
    SAVINGS = "savings", "Savings" 
    INVESTING = "investing", "Investing" 
    OTHER = "other", "Other" 

class MoneyAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=make_uuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=255, null=True, blank=True, default=defaultname)
    bank = models.CharField(max_length=255, null=True, blank=True)
    account_type = models.CharField(max_length=50, null=False, choices=AccountTypes.choices, default=AccountTypes.PERSONAL)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TransactionTypes(models.TextChoices):
    """Enumeration for the types of questions"""

    PAYMENT = "payment", "Payment" 
    DEPOSIT = "deposit", "Deposit" 

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=make_uuid)
    title = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    account = models.ForeignKey(MoneyAccount, on_delete=models.CASCADE, related_name="transactions")
    current_balance = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    new_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    transaction_type = models.CharField(max_length=50, null=False, choices=TransactionTypes.choices)
    

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

