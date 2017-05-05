# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework import routers
from .views import BillViewSet, ExpenseViewSet, MemoViewSet


router = routers.DefaultRouter()
router.register(r'bills', BillViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'memo', MemoViewSet)

urlpatterns = router.urls