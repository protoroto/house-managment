# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Bill, Expense, Memo


class BillAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'cost', 'expiry_date', 'payed', 'person', 'payed_date',
    )
    list_filter = ('expiry_date', 'payed', 'payed_date', 'person')
    fieldsets = (
        ('Dati bolletta', {
            'fields': (('title', 'cost', 'expiry_date'), ('payed', 'person', 'payed_date', 'payed_image'),)
        }),
    )

admin.site.register(Bill, BillAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'cost', 'payed_date', 'person'
    )
    list_filter = ('person',)
    fieldsets = (
        ('Dati spesa', {
            'fields': (('title', 'cost', 'payed_date', 'person'))
        }),
    )

admin.site.register(Expense, ExpenseAdmin)


class MemoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'cost', 'expiry_date',
    )
    list_filter = ('expiry_date',)
    fieldsets = (
        ('Dati memo', {
            'fields': (('title', 'cost', 'expiry_date'))
        }),
    )

admin.site.register(Memo, MemoAdmin)
