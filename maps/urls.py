from django.conf.urls import url

from maps.views import *

urlpatterns = [
    url(r'^create$', map_create, name="map_create"),
    url(r'^all$', map_all, name="all"),
    url(r'^(?P<map_id>[0-9]+)/lesson/create/$', lesson_create, name="lesson_create"),
    url(r'^(?P<map_id>[0-9]+)/lessons/$', lessons_list, name='lessons'),
    url(r'^(?P<map_id>[0-9]+)/lesson/(?P<lesson_id>\d+)/$', lesson_page, name='lesson_page'),
    url(r'^(?P<map_id>[0-9]+)/lesson/(?P<lesson_id>\d+)/question/create/$', question_create, name='question_create'),
    url(r'^(?P<map_id>[0-9]+)/lesson/(?P<lesson_id>\d+)/questions/$', question_list, name='questions'),
    url(r'^(?P<map_id>[0-9]+)/lesson/(?P<lesson_id>\d+)/test/$', lesson_test, name='lesson_test'),

]