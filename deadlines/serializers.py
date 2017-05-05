from rest_framework import serializers
from .models import Bill, Expense, Memo


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('title', 'cost', 'expiry_date', 'payed', 'person', 'get_person', 'payed_date', 'payed_image')


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        fields = '__all__'
