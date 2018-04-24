from django.core import serializers
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from .models import Content


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
        context['result_len'] = result_len
        context['result_json'] = serializers.serialize(
            "json", Content.objects.all()[:self.display_count])
        return context


def spider_result_ajax(request, start_count, end_count):
    result = serializers.serialize(
        "json", Content.objects.all()[start_count:end_count])
    return JsonResponse(result, safe=False)
