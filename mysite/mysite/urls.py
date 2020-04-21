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

from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view

urlpatterns = [
    url(r'^', include('luke.urls')),
    url(r'^admin/', admin.site.urls),

    # In Django 1.9+, REST framework will set the namespace, so you may leave it out.
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # for clients to obtain a token given the username and password.
    url(r'^api-token-auth/', views.obtain_auth_token),

    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    # See: https://www.django-rest-framework.org/api-guide/schemas/
    # Dependences:
    #   $ pip install pyyaml uritemplate
    path('openapi', get_schema_view(
        title="Luke",
        description="API for all things",
        version="1.0.0"
    ), name='openapi-schema'),

    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
