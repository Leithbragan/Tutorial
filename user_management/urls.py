from django.conf.urls import url
from user_management.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^registration$', user_registretion, name="registration"),
    url(r'^profile/', profile, name="profile"),
    url(r'^login/', login_view, name="login"),
    url(r'^logout$', auth_views.logout, {'next_page': '/login'}, name='logout'),
]