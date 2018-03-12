"""bitrix24first URL Configuration"""
from django.conf.urls import url, include
#from django.contrib import admin

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^filling/', include('filling.urls')),
    url(r'', include('doubles.urls'))
]
