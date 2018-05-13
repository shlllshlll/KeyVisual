# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-15 21:27:55
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-16 00:54:57
# @License: MIT LICENSE

import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = (timezone.now() -
                datetime.timedelta(hours=23, minutes=59, seconds=59))
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        # 测试如果没有问题存在的话，是否显示了合适的信息
        response = self.client.get(reverse('client:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No client are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # 测试过去的问题是否被显示
        create_question("Past question", days=-30)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question>'])

    def test_future_question(self):
        # 测试未来的问题是否不会被显示
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('client:index'))
        self.assertContains(response, "No client are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        # 测试当同时存在未来和过去的问题的时候只显示过去的问题
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_past_two_question(self):
        # 测试当同时存在两个过去的问题的时候是否正确显示
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('client:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('client:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
