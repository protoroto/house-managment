# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Bill, Expense, Memo


class BillSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(format='%d/%m/%Y')
    payed_date = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = Bill
        fields = ('pk', 'title', 'cost', 'expiry_date', 'payed', 'person', 'get_person',
                  'payed_date', 'payed_image')


class ExpenseSerializer(serializers.ModelSerializer):
    payed_date = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = Expense
        fields = ('pk', 'title', 'cost', 'payed_date', 'person', 'get_person')


class MemoSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'cost', 'expiry_date')
