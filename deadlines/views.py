from django.views.generic.list import ListView

from .models import Bill, Expense, Memo


class BillListView(ListView):

    model = Bill
    context_object_name = 'bills'

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        context['expenses'] = Expense.objects.all()
        context['memo'] = Memo.objects.all()
        return context
