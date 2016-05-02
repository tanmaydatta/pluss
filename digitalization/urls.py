from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^add/$', add, name='add'),

]
