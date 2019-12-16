from django.conf.urls import url
from .views import stockviewcache
 
urlpatterns = [
    url('', stockviewcache),
]