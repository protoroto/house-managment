from django.shortcuts import redirect
from django.views.generic.list import ListView
from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, mixins, status

from .models import Bill, Expense, Memo
from .serializers import BillSerializer, ExpenseSerializer, MemoSerializer


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer


class HouseManagementList(APIView):

	renderer_classes = (TemplateHTMLRenderer,)
	template_name='deadlines/bill_list.html'
    
	def get(self, request, format=None):
		bills = Bill.objects.all()
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

	renderer_classes = (TemplateHTMLRenderer,)
	template_name = 'deadlines/bills.html'

	def get(self, request, format=None):
		bills = Bill.objects.all()
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