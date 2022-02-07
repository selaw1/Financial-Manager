import datetime
import imp
from threading import main_thread
from unicodedata import decimal
from urllib import request
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

from moneyaccount.forms.filters import TransactionFilterForm
from moneyaccount.forms.accounts import RegistrationForm
from moneyaccount.models import MoneyAccount, Transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        """get context"""
        context = super().get_context_data(**kwargs)

        valid = False
        try:
            all_transactions = Transaction.objects.filter(account__user=self.request.user)
            main_moneyaccount = MoneyAccount.objects.get(Q(is_main=True) & Q(user=self.request.user))
        except MoneyAccount.DoesNotExist:
            main_moneyaccount = None

        form = TransactionFilterForm(self.request.GET.dict())
        if form.is_valid():
            valid = True
            
            filter = form.cleaned_data["filter"]
            search = form.cleaned_data["search"]

            if filter == "today":
                date = datetime.date.today()
                all_transactions = all_transactions.filter(date__gte=date)

            if filter == "week":
                date = datetime.date.today() - datetime.timedelta(days=7)
                all_transactions = all_transactions.filter(date__gte=date)

            if filter == "month":
                date = datetime.date.today() - datetime.timedelta(days=30)
                all_transactions = all_transactions.filter(date__gte=date)

            if search:
                all_transactions =all_transactions.filter(
                    Q(title__icontains=search) |
                    Q(amount__icontains=search) | 
                    Q(account__name__icontains=search)
                )

        context["transactions"] = all_transactions[:15]
        context["main_account"] = main_moneyaccount
        context["valid"] = valid
        return context

class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('mc:login')

    def form_valid(self, form):
        user = form.save(self.request)

        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Created!'
        ) 
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('mc:dashboard'))
        return super().dispatch(request, *args, **kwargs)
