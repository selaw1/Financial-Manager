from django.contrib import admin

from moneyaccount.models import MoneyAccount, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'account', 'date' ]
    readonly_fields = ['id']

@admin.register(MoneyAccount)
class MoneyAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_balance', 'user', 'is_main']
    readonly_fields = ['id']

    fieldsets = (
        ('Account Information', {"fields": ('name', 'user', 'id')}),
        ('Other Details', {"fields": ('total_balance', 'account_type', 'bank', 'is_main'), "classes": ('collapse',)})
    )

    list_filter = ['is_main', 'account_type']
    search_fields = ['user__username', 'name', 'id', 'total_balance']
