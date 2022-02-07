import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from moneyaccount.models import MoneyAccount, Transaction


class ExportTransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MoneyAccount
    template_name = "reports.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def test_func(self):
        my_accounts = self.get_queryset()
        my_accounts_check = [ account.user == self.request.user for account in my_accounts]
        return all(my_accounts_check)

class ExportTransactionView(LoginRequiredMixin, View):
    """Generate CSV file for Transactions"""

    template_name = "transaction/export_transaction.html"
    TRANSACTION_HEADER = [
        'Account Name',
        "Title",
        "Note",
        "Current Balance",
        "Amount",
        "Total",
        "Date",
        "Transaction Type",
    ]

    def get(self, request, *args, **kwargs):
        """get context"""
        context = {
            "accounts": MoneyAccount.objects.filter(user=self.request.user),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        accounts = MoneyAccount.objects.filter(user=self.request.user)

        for account in accounts:
            if account.name in request.POST:
                file_name = f"{account.name}.csv"
                transactions = account.transactions.order_by("date")
                
                response = None
                if transactions:
                    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
                    writer = csv.writer(response)
                    writer.writerow(self.TRANSACTION_HEADER)

                    for transaction in transactions:
                        writer.writerow(
                            [
                                account.name,
                                transaction.title,
                                transaction.note,
                                transaction.current_balance,
                                transaction.amount,
                                transaction.new_balance,
                                transaction.date,
                                transaction.transaction_type,
                            ]
                        )

                    response["Content-Disposition"] = f"attachment; filename={file_name}"
                    return response
            return redirect(reverse_lazy("mc:report-list"))
