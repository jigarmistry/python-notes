from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^study/', include('practice.urls')),
    url(r'^admin/', admin.site.urls),
]
