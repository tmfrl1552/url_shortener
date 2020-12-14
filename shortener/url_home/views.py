from django.shortcuts import render, redirect
from .models import Url
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.views import View
from django.views import generic
# Create your views here.

class Url_home(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'url_home/index.html'

        return render(request, template_name)


@csrf_exempt
def shorten_post(request):
    origin_url = request.POST['url']
    url_obj = create_shorten(origin_url)
    context = {'shorten_url': url_obj.shorten_url, 'origin_url': url_obj.origin_url}
    return render(request, 'url_home/index.html', context)


#url 단축
def create_shorten(origin_url):
        origin_url = make_full_addr(origin_url)

        try:
            exist_url_obj = Url.objects.get(origin_url = origin_url)
        except Url.DoesNotExist:
            exist_url_obj = None

        if exist_url_obj is not None:
            return exist_url_obj

        if Url.objects.all().count() == 0:
            id = 1
        else:
            obj = Url.objects.order_by('key').last()
            id = obj.key + 1

        shorten_url = encode(id)

        url_obj = Url(
            key=id,
            origin_url=origin_url,
            shorten_url='http://localhost:8000/'+shorten_url,
        )
        url_obj.save()
        return url_obj


# shorten_url로 접근 시 원래의 url로 return
@api_view(['GET'])
def redirect_origin_url(request, **kwargs):
    shorten = kwargs.get('shorten')
    id = decode(shorten)
    try:
        url = Url.objects.get(key=id)
    except:
        return Response({
            'resonse': 'error',
            'message': f'{shorten}에 해당하는 url이 존재하지 않습니다.'
        })

    return redirect(url.origin_url)


#10진수 -> 62진수로 변경
def encode(id):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    ret = []
    while id > 0:
        val = id % base
        ret.append(characters[val])
        id = id // base

    return "".join(ret[::-1])


#62진수 -> 10진수로 변환
def decode(inputStr):
    T = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = 0
    for idx, c in enumerate(reversed(inputStr)):
        num = T.find(c)
        result += num * (62 ** idx)
    return result


#http가 없는 경우 url 추가
def make_full_addr(origin_url):
        if origin_url[:4] != 'http':
            origin_url = 'http//' + origin_url
        return origin_url