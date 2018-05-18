from . import views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(r'^home/', include('src.home.urls', namespace='home')),
    url(r'^administration/', include('src.administration.urls', namespace='administration')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
