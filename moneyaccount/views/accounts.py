from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages

from moneyaccount.forms.accounts import MoneyAccountForm
from moneyaccount.models import MoneyAccount


# Money Account
class MoneyAccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MoneyAccount
    template_name = 'moneyaccount/account_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def test_func(self):
        my_accounts = self.get_queryset()
        my_accounts_check = [ account.user == self.request.user for account in my_accounts]
        return all(my_accounts_check)

class MoneyAccountCreateView(LoginRequiredMixin, CreateView):
    model = MoneyAccount
    form_class = MoneyAccountForm
    template_name = 'moneyaccount/account_create.html'
    success_url = reverse_lazy('mc:account-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Account Created!'
        ) 
        return super().form_valid(form)

class MoneyAccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MoneyAccount
    form_class = MoneyAccountForm
    template_name = 'moneyaccount/account_update.html'
    success_url = reverse_lazy('mc:account-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        name = form.cleaned_data['name']

        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Account({name}) Updated!'
        ) 
        return super().form_valid(form)

    def test_func(self):
        account = self.get_object()
        return True if self.request.user == account.user else False

class MoneyAccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MoneyAccount
    template_name = 'moneyaccount/account_detail.html'

    def test_func(self):
        account = self.get_object()
        return True if self.request.user == account.user else False

class MoneyAccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MoneyAccount
    template_name = 'moneyaccount/account_delete.html'

    def test_func(self):
        account = self.get_object()
        return True if self.request.user == account.user else False

    def get_success_url(self):
        return reverse_lazy('mc:account-list')

def make_main(request, account_pk):
    account = get_object_or_404(MoneyAccount, id=account_pk)
    main_account = MoneyAccount.objects.get(user=account.user, is_main=True)
    
    if main_account:
        main_account.is_main = False
        main_account.save()
    
    account.is_main = True
    account.save()

    return redirect(reverse_lazy("mc:account-detail", kwargs={'name':account.name, "pk":account_pk}))
