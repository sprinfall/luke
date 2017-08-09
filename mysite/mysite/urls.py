"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.authtoken import views


urlpatterns = [
    url(r'^', include('luke.urls')),
    url(r'^admin/', admin.site.urls),

    # In Django 1.9+, REST framework will set the namespace, so you may leave it out.
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # for clients to obtain a token given the username and password.
    url(r'^api-token-auth/', views.obtain_auth_token),

]
