from django.conf.urls import url

from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'preview_source_online$', views.preview_source_online, name='preview_source_online'),
]