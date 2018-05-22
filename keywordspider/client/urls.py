# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 21:32:35
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-22 15:40:37
# @License: MIT LICENSE

from django.urls import path
from . import views


app_name = "client"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.SpiderResultView.as_view(), name='result'),
    path('result/<int:start_count>/<int:end_count>',
         views.spider_result_ajax, name='result_ajax'),
    path('control/', views.SpiderControlView.as_view(), name='control'),
    path('control/post/', views.spider_control_post, name='control_post'),
    path('control/status/', views.spider_control_status_ajax, name='control_status'),
    path('control/result/', views.spider_control_result_ajax, name='control_result'),
    path('keyword/', views.KeywordView.as_view(), name='keyword'),
    path('keyword/<int:start_count>/<int:end_count>',
         views.keyword_ajax, name='keyword_ajax'),
    path('assocword/', views.AssocwordView.as_view(), name='assocword'),
    path('assocword/len/<str:cur_tab>',
         views.assocword_len_ajax, name='assocword_len_ajax'),
    path('assocword/<str:cur_tab>/<int:start_count>/<int:end_count>',
         views.assocword_ajax, name='assocword_ajax')
]
