"""webshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

import settings
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path(r'api-token-auth/', obtain_jwt_token, name='api_token_auth'),
    path(r'api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('api/', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]
