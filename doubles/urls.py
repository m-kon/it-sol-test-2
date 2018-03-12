from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^get_bitrix/$', views.get_bitrix_doubles),
    url(r'^$', TemplateView.as_view(template_name='doubles/index.html'))
]
