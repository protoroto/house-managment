from django.views.generic.list import ListView
from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status

from .models import Bill, Expense, Memo
from .serializers import BillSerializer, ExpenseSerializer, MemoSerializer



class BillListView(ListView):

    model = Bill
    context_object_name = 'bills'

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        return context


class HouseManagementList(APIView):

	renderer_classes = (TemplateHTMLRenderer,)
    
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
		}, template_name='deadlines/bill_list.html')


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer