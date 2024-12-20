"""mimicINT URL Configuration

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
from django.urls import path
from django.conf.urls import url, include, re_path
from mimicINTapp.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home', ),
    url(r'^jobs$', jobs, name='jobs'),
    url(r'^prediction$', form, name='form'),
    url(r'^prediction/run$', pre_pipeline, name='pre_pipeline'),
    url(r'^prediction/(?P<run_id>\w*)$', pipeline, name='pipeline'),   
    url(r'^results$', result, name='result'),
    url(r'^results/(?P<job_id>\w*)$', result, name='results'),
    path('results/progress/<job_id>/', progress, name='progress'),
    
    path('results/<job_id>/<json_filename>', table_json, name='table_json'),
    path('results/<job_id>/query_disorder_prop.json', table1, name='table1'),
   
    url(r'^cytoscape$', cytoscape, name='cyto'),
    url(r'^cytoscape/(?P<job_id>\w*)$', cytoscape, name='cytoscape'),
    url(r'^tutorial$', tutorial, name='tutorial'),
    url(r'download_zip/(?P<job_id>\w*)$', download_zip, name='download_zip'),
    url(r'^about$', about, name='about'),
    url(r'^documentation$', documentation, name='documentation')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

