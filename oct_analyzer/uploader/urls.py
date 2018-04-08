from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^compare',views.compare_scans,name='compare'),
    url(r'^post_upload',views.post_upload,name='post_upload'),
    url(r'^$', views.model_form_upload, name='model_form_upload'),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)