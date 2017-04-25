from rest_framework import serializers
from .models import Bill, Expense, Memo


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        fields = '__all__'