from django.core import serializers
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from .models import Content, Keyword, Frequent, Confidence


class IndexView(TemplateView):
    template_name = "client/index.html"


class SpiderResultView(ListView):
    template_name = "client/result.html"
    model = Content   # 定义数据模型
    context_object_name = "result_list"  # 定义模板中的变量名
    display_count = 15

    def get_context_data(self, **kwargs):
        # 将额外的数据添加到上下文数据中
        context = super().get_context_data(**kwargs)
        result_len = len(Content.objects.all())
        context['result_title'] = ["标题", "发布日期", "新闻"]
        context['result_len'] = result_len
        context['result_json'] = serializers.serialize(
            "json", Content.objects.all()[:self.display_count])
        return context


def spider_result_ajax(request, start_count, end_count):
    result = serializers.serialize(
        "json", Content.objects.all()[start_count:end_count])
    return JsonResponse(result, safe=False)


class KeywordView(ListView):
    template_name = "client/keyword.html"
    model = Keyword   # 定义数据模型
    context_object_name = "result_list"  # 定义模板中的变量名
    display_count = 15

    def get_context_data(self, **kwargs):
        # 将额外的数据添加到上下文数据中
        context = super().get_context_data(**kwargs)
        result_len = len(Keyword.objects.all())
        context['result_title'] = ["标题", "关键词"]
        context['result_len'] = result_len
        context['result_json'] = serializers.serialize(
            "json", Keyword.objects.all()[:self.display_count])
        return context


def keyword_ajax(request, start_count, end_count):
    result = serializers.serialize(
        "json", Keyword.objects.all()[start_count:end_count])
    return JsonResponse(result, safe=False)


class AssocwordView(ListView):
    template_name = "client/assocword.html"
    model = Frequent   # 定义数据模型
    context_object_name = "result_list"  # 定义模板中的变量名
    display_count = 15

    def get_context_data(self, **kwargs):
        # 将额外的数据添加到上下文数据中
        context = super().get_context_data(**kwargs)
        result_len = len(Frequent.objects.all())
        context['result_display'] = ["itemsets", "support"]
        context['result_title'] = ["关键词", "支持度"]
        context['result_len'] = result_len
        context['result_json'] = serializers.serialize(
            "json", Frequent.objects.all()[:self.display_count])
        return context


def assocword_len_ajax(request, cur_tab):
    if cur_tab == "freq":
        length = len(Frequent.objects.all())
        title = ["关键词", "支持度"]
        display = ["itemsets", "support"]
    elif cur_tab == "assoc":
        length = len(Confidence.objects.all())
        title = ["后项规则", "前向规则", "置信度"]
        display = ["back_item", "front_item", "confidence"]
    return JsonResponse({"len": length, "title": title, "display": display})


def assocword_ajax(request, cur_tab, start_count, end_count):
    if cur_tab == "freq":
        model = Frequent
    elif cur_tab == "assoc":
        model = Confidence

    result = serializers.serialize(
        "json", model.objects.all()[start_count:end_count])
    return JsonResponse(result, safe=False)
