# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Bill, Expense, Memo


class BillSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(
        label=_(u"Data scadenza"), 
    )
    payed_date = serializers.DateField(
        label=_(u"Data pagamento"), 
        required=False
    )

    class Meta:
        model = Bill
        fields = ('pk', 'title', 'cost', 'expiry_date', 'payed', 'person', 'get_person',
                  'payed_date', 'payed_image')


class ExpenseSerializer(serializers.ModelSerializer):
    payed_date = serializers.DateField(
        label=_(u"Data pagamento"), 
    )

    class Meta:
        model = Expense
        fields = ('pk', 'title', 'cost', 'payed_date', 'person', 'get_person')


class MemoSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(
        label=_(u"Data scadenza"), 
        required=False
    )

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'cost', 'expiry_date')
