# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 21:32:35
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-11 16:34:34
# @License: MIT LICENSE

from django.urls import path
from . import views

urlpatterns = [
    # ex: /app/
    path('', views.index, name='index'),
    # ex: /app/5/
    path('<int:question_id>/', views.detial, name='detail'),
    # ex: /app/5/results/
    path('<int:question_id>/results', views.results, name='results'),
    # ex: /app/5/vote/
    path('<int:question_id>/vote', views.vote, name='vote')
]