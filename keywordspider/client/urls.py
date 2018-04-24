# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 21:32:35
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-22 21:48:34
# @License: MIT LICENSE

from django.urls import path
from . import views


app_name = "client"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.SpiderResultView.as_view(), name='result'),
    path('result/<int:start_count>/<int:end_count>',
         views.spider_result_ajax, name='result_ajax')
]
