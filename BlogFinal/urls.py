
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', inicio),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)