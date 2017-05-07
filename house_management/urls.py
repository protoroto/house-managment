# -*- coding: utf-8 -*-
"""house_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from deadlines.views import (
    BillDetail, BillList, ExpenseDetail, ExpenseList, HouseManagementList, MemoDetail, MemoList
)

import deadlines


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('deadlines.urls', namespace='deadlines')),
    url(r'^bills/$', BillList.as_view(), name='bills'),
    url(r'^bills/(?P<pk>[0-9]+)/$', BillDetail.as_view(), name='bill-detail'),
    url(r'^expenses/$', ExpenseList.as_view(), name='expenses'),
    url(r'^expenses/(?P<pk>[0-9]+)/$', ExpenseDetail.as_view(), name='expense-detail'),
    url(r'^memo/$', MemoList.as_view(), name='memo'),
    url(r'^memo/(?P<pk>[0-9]+)/$', MemoDetail.as_view(), name='memo-detail'),
    url(r'^$', HouseManagementList.as_view(), name='bills-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
