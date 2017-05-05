from django.shortcuts import redirect
from django.views.generic.list import ListView
from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from .models import Bill, Expense, Memo
from .serializers import BillSerializer, ExpenseSerializer, MemoSerializer


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
	filter_fields = ('cost', 'person',)
	ordering_fields = ('cost', 'payed_date')


class MemoViewSet(viewsets.ModelViewSet):
	queryset = Memo.objects.all()
	serializer_class = MemoSerializer
	filter_backends = (OrderingFilter,)
	ordering_fields = ('cost', 'expiry_date')


class HouseManagementList(APIView):

	renderer_classes = (TemplateHTMLRenderer,)
	template_name='deadlines/bill_list.html'

	def get(self, request, format=None):
		bills = Bill.objects.filter(payed=False)
		expenses = Expense.objects.all()
		memo = Memo.objects.all()
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
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('payed',)

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

	renderer_classes = (TemplateHTMLRenderer,)
	template_name = 'deadlines/expenses.html'

	def get(self, request, format=None):
		expenses = Expense.objects.all()
		expense_serializer = ExpenseSerializer(expenses, many=True)
		form_serializer = ExpenseSerializer
		return Response({
			'expenses': expense_serializer.data,
			'serializer': form_serializer
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
