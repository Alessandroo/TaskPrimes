from django.conf.urls import url
from django.contrib import admin
from Primes import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_prime/', views.browser),
    url(r'^$', views.index),
]