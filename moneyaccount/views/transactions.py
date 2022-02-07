import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from django.contrib import messages
from django.db.models import Q, F
from moneyaccount.forms.filters import TransactionFilterForm
from moneyaccount.forms.transactions import TransactionForm

from moneyaccount.models import MoneyAccount, Transaction, TransactionTypes

# Transactions
class TransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(account__user=self.request.user) & Q(account__id=self.kwargs['account_pk']))
        
        form = TransactionFilterForm(self.request.GET.dict())
        if form.is_valid():
            
            filter = form.cleaned_data["filter"]
            search = form.cleaned_data["search"]
            
            if filter == "today":
                date = datetime.date.today()
                queryset = queryset.filter(date__gte=date)

            if filter == "week":
                date = datetime.date.today() - datetime.timedelta(days=7)
                queryset = queryset.filter(date__gte=date)

            if filter == "month":
                date = datetime.date.today() - datetime.timedelta(days=30)
                queryset = queryset.filter(date__gte=date)

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(amount__icontains=search)
                )
        else:
            queryset = None
        return queryset


    def test_func(self):
        account = MoneyAccount.objects.get(pk=self.kwargs['account_pk'])
        return True if self.request.user == account.user else False

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/transaction_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        account = MoneyAccount.objects.get(id=self.kwargs['account_pk'])
        context['account'] = account
        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)

        account = MoneyAccount.objects.get(id=self.kwargs['account_pk'])
        transaction.account = account
        transaction.current_balance = account.total_balance

        if 'payment' in self.request.POST:
            transaction.transaction_type = TransactionTypes.PAYMENT
            account_pay(transaction, account)
            transaction.new_balance = transaction.current_balance - transaction.amount

        if 'deposit' in self.request.POST:
            transaction.transaction_type = TransactionTypes.DEPOSIT
            account_deposit(transaction, account)
            transaction.new_balance = transaction.current_balance + transaction.amount

        transaction.save()

        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Transaction Successful!'
        ) 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mc:transaction-list', kwargs={'name':self.kwargs["name"], 'account_pk':self.kwargs["account_pk"]})

def account_pay(transaction, account):
    account.total_balance = F("total_balance") - transaction.amount
    account.save()

def account_deposit(transaction, account):
    account.total_balance = F("total_balance") + transaction.amount
    account.save()

class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'

    def form_valid(self, form):
        transaction = self.get_object()
        account = MoneyAccount.objects.get(id=self.kwargs['account_pk'])

        if transaction.transaction_type == TransactionTypes.PAYMENT:
            account.total_balance = F("total_balance") + transaction.amount 
            account.save()

        if transaction.transaction_type == TransactionTypes.DEPOSIT:
            account.total_balance = F("total_balance") - transaction.amount
            account.save()
        
        transaction.delete()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse_lazy('mc:transaction-list', kwargs={'name':self.kwargs["name"], 'account_pk':self.kwargs["account_pk"]})

    def test_func(self):
        transaction = self.get_object()
        return True if self.request.user == transaction.account.user else False

class TransactionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Transaction
    template_name = "transaction/transaction_detail.html"
    
    def test_func(self):
        transaction = self.get_object()
        return True if self.request.user == transaction.account.user else False
