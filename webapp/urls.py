from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from eroge import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
] + static('/pictures/', document_root=(settings.OUR_ROOT / 'pictures').as_posix())
