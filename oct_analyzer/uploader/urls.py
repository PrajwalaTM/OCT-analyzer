from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^post_upload',views.post_upload,name='post_upload'),
    url(r'^$', views.model_form_upload, name='model_form_upload'),  
]