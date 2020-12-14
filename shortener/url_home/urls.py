from django.conf.urls import url
from django.urls import path, include
from . import views


from django.conf import settings
from django.conf.urls.static import static

app_name = 'url_home'

urlpatterns = [
    url(r'^$', views.Url_home.as_view(), name='url_home'),
    url(r'^shorten/$', views.shorten_post, name='url_home_shorten'),
    path('<str:shorten>/', views.redirect_origin_url),
]
