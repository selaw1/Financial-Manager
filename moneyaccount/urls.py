
from django.urls import path
from django.contrib.auth import views as auth_views

from moneyaccount.views import dashboard, accounts, transactions, reports


app_name = "mc"

urlpatterns = [
    path('dashboard/', dashboard.DashboardView.as_view(), name="dashboard"),
    # Money Accounts
    path('my-accounts/', accounts.MoneyAccountListView.as_view(), name="account-list"),
    path('my-accounts/create/', accounts.MoneyAccountCreateView.as_view(), name="account-create"),
    path('my-accounts/update/<str:name>/<uuid:pk>/', accounts.MoneyAccountUpdateView.as_view(), name="account-update"),
    path('my-accounts/<str:name>/<uuid:pk>/', accounts.MoneyAccountDetailView.as_view(), name="account-detail"),
    path('my-accounts/delete/<str:name>/<uuid:pk>/', accounts.MoneyAccountDeleteView.as_view(), name="account-delete"),
    path('make-main/<uuid:account_pk>/', accounts.make_main, name="make-main"),
    # Transactions
    path('my-accounts/<str:name>/<uuid:account_pk>/transactions/', transactions.TransactionListView.as_view(), name="transaction-list"),
    path('my-accounts/<str:name>/<uuid:account_pk>/transactions/create/', transactions.TransactionCreateView.as_view(), name="transaction-create"),
    path('my-accounts/<str:name>/<uuid:account_pk>/transactions/delete/<uuid:pk>', transactions.TransactionDeleteView.as_view(), name="transaction-delete"),
    path('my-accounts/<str:name>/<uuid:account_pk>/transactions/detail/<uuid:pk>', transactions.TransactionDetailView.as_view(), name="transaction-detail"),
    # Export Reports
    path('reports/', reports.ExportTransactionListView.as_view(), name="report-list"),
    path('reports/export/<uuid:account_pk>/', reports.ExportTransactionView.as_view(), name="export-report"),
    # User Accounts
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True) ,name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', dashboard.UserCreateView.as_view(), name='register'),
]
