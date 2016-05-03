from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^search/$', search, name='search'),
    url(r'^add/$', add, name='add'),
    url(r'^get_product/$', get_product, name='get_product'),

]
