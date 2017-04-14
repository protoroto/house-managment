from django.views.generic.list import ListView

from .models import Bill


class BillListView(ListView):

    model = Bill

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        return context
