"""perf_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index_page"),
    url(r'^admin/', admin.site.urls),
    url(r'^release_builds/', include('release_builds.urls')),
    url(r'^configurations/', include('configurations.urls')),
    url(r'^artifacts/', include('artifacts.urls')),
    url(r'^regression_alerts/', include('regression_alerts.urls')),
    url(r'^benchmarks/', include('benchmarks.urls')),
]

urlpatterns += staticfiles_urlpatterns()
