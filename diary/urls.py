from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register, diary_create, diary_list, diary_delete, diary_update, user_login, public, diary_detail, test, update_profile, change_password
from .views import contact

urlpatterns = [
    url(r'^$', home),
    url(r'^test/$', test),
    url(r'^update_profile/$', update_profile),
    url(r'^register/', register),
    url(r'^contact/', contact),
    url(r'^change_password/$', change_password, name='change_password'),
    url(r'^public/', public, name='public'),
    url(r'^login/', user_login),
    url(r'^list/$', diary_list, name='list'),
    url(r'^create/$', diary_create, name='create'),
    url(r'^(?P<id>[\w-]+)/edit/$', diary_update, name='update'),
    url(r'^(?P<id>[\w-]+)/delete/$', diary_delete,name='delete'),
    url(r'^(?P<id>[\w-]+)/detail/$', diary_detail, name='detail'),
]
