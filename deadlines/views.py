# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.db.models import Sum
from django_filters import rest_framework as filters
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.filters import OrderingFilter

from .models import Bill, Expense, Memo, MONTHS
from .serializers import BillSerializer, ExpenseSerializer, MemoSerializer


class ExpenseFilter(filters.FilterSet):
    class Meta:
        model = Expense
        fields = {'payed_date': ['gt', 'lt']}


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('payed',)
    ordering_fields = ('cost', 'expiry_date')


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('cost', 'person', 'payed_date',)
    filter_class = ExpenseFilter
    ordering_fields = ('cost', 'payed_date')


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('cost', 'expiry_date')


class HouseManagementList(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name='deadlines/general_list.html'

    def get(self, request, format=None):
        bills = Bill.objects.all()[:settings.ENTRY_NUMBER_IN_HOME]
        expenses = Expense.objects.all()[:settings.ENTRY_NUMBER_IN_HOME]
        memo = Memo.objects.all()[:settings.ENTRY_NUMBER_IN_HOME]
        bills_serializer = BillSerializer(bills, many=True)
        expenses_serializer = ExpenseSerializer(expenses, many=True)
        memo_serializer = MemoSerializer(memo, many=True)

        return Response({
            'bills': bills_serializer.data,
            'expenses': expenses_serializer.data,
            'memos': memo_serializer.data,
        })


class BillList(APIView):

    serializer_class = BillSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/bills.html'

    def get(self, request, format=None):
        bills = Bill.objects.all()
        payed = self.request.query_params.get('payed', None)
        if payed is not None:
            bills = bills.filter(payed=payed.capitalize())
        bill_serializer = BillSerializer(bills, many=True)
        form_serializer = BillSerializer
        return Response({
            'bills': bill_serializer.data,
            'serializer': form_serializer
        })

    def post(self, request, format=None):
        bills = Bill.objects.all()
        bill_serializer = BillSerializer(bills, many=True)
        form_serializer = BillSerializer(data=request.data)
        if form_serializer.is_valid():
            form_serializer.save()
            return redirect('bills')
        return Response({
            'bills': bill_serializer.data,
            'serializer': form_serializer
        }, status=status.HTTP_400_BAD_REQUEST)


class ExpenseList(APIView):
    '''
    List all expenses from current month: if payed_date__month query parameter is present
    list all expenses from that month (and the two sum accordingly)
    '''

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/expenses.html'

    def get(self, request, format=None):
        '''
        If query_params has payed_date__month return the expenses and the total expenses per person
        of that month, otherwise return current month expenses and totals.
        '''
        this_month = now().month
        payed_date_month = self.request.query_params.get('payed_date__month')
        if payed_date_month:
            expenses = Expense.objects.filter(payed_date__month=payed_date_month)
        else:
            expenses = Expense.objects.filter(payed_date__month=this_month)
        total_expenses_leo = expenses.filter(
            person='L').filter(
            payed_date__month=payed_date_month if payed_date_month else this_month).aggregate(
            total_leo=Sum('cost'))
        total_expenses_isa = expenses.filter(
            person='I').filter(
            payed_date__month=payed_date_month if payed_date_month else this_month).aggregate(
            total_isa=Sum('cost'))
        expenses_leo = total_expenses_leo['total_leo'] or Decimal(0)
        expenses_isa = total_expenses_isa['total_isa'] or Decimal(0)

        month_selected = this_month if not payed_date_month else payed_date_month

        difference = abs((expenses_leo - expenses_isa) / 2) if expenses_leo or expenses_isa else 0

        expense_serializer = ExpenseSerializer(expenses, many=True)
        form_serializer = ExpenseSerializer

        return Response({
            'expenses': expense_serializer.data,
            'serializer': form_serializer,
            'total_leo': expenses_leo,
            'total_isa': expenses_isa,
            'difference': difference,
            'months': MONTHS,
            'month_selected': month_selected,
        })

    def post(self, request, format=None):
        expenses = Expense.objects.all()
        expense_serializer = ExpenseSerializer(expenses, many=True)
        form_serializer = ExpenseSerializer(data=request.data)
        if form_serializer.is_valid():
            form_serializer.save()
            return redirect('expenses')
        return Response({
            'expenses': expense_serializer.data,
            'serializer': form_serializer
        }, status=status.HTTP_400_BAD_REQUEST)


class MemoList(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/memo.html'

    def get(self, request, format=None):
        memo = Memo.objects.all()
        memo_serializer = MemoSerializer(memo, many=True)
        form_serializer = MemoSerializer
        return Response({
            'memos': memo_serializer.data,
            'serializer': form_serializer
        })

    def post(self, request, format=None):
        memo = Memo.objects.all()
        memo_serializer = MemoSerializer(memo, many=True)
        form_serializer = MemoSerializer(data=request.data)
        if form_serializer.is_valid():
            form_serializer.save()
            return redirect('memo')
        return Response({
            'memos': memo_serializer.data,
            'serializer': form_serializer
        }, status=status.HTTP_400_BAD_REQUEST)


class BillDetail(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/bill_detail.html'

    def get(self, request, pk, format=None):
        bill = get_object_or_404(Bill, pk=pk)
        serializer = BillSerializer(bill)
        return Response({'serializer': serializer, 'bill': bill})

    def post(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        serializer = BillSerializer(bill, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'bill': bill})
        serializer.save()
        return redirect('bills')


class ExpenseDetail(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/expense_detail.html'

    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response({'serializer': serializer, 'expense': expense})

    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'expense': expense})
        serializer.save()
        return redirect('expenses')


class MemoDetail(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'deadlines/memo_detail.html'

    def get(self, request, pk):
        memo = get_object_or_404(Memo, pk=pk)
        serializer = MemoSerializer(memo)
        return Response({'serializer': serializer, 'memo': memo})

    def post(self, request, pk):
        memo = get_object_or_404(Memo, pk=pk)
        serializer = MemoSerializer(memo, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'memo': memo})
        serializer.save()
        return redirect('memo')
