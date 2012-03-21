from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.views.generic import list_detail
from eiga.models import Article
from eiga.views import InCinemasListView
from eiga.views import OutToBuyListView
from eiga.views import ComingSoonListView
from eiga import views
from django.conf import settings
from datetime import datetime, timedelta

from django.contrib import admin
admin.autodiscover()

review_detail_info = {
    'queryset': Article.objects.all(),
    "template_name" : "eiga/review_detail.html",
    "template_object_name" : "review",
}

urlpatterns = patterns('',
    (r'^home/$', views.home),
    (r'^incinemas/$', InCinemasListView.as_view()),
    (r'^comingsoon/$', ComingSoonListView.as_view()),
    (r'^outtobuy/$', OutToBuyListView.as_view()),
    (r'^outtobuy/(?P<object_id>\d+)/$', views.outtobuy_detail),
    (r'^reviewarchive/$', views.archive_listing),
    (r'^reviewarchive/viewall/', views.archive_listing, {'page_size': -1}),
    (r'^reviews/(?P<object_id>\d+)/$', list_detail.object_detail, review_detail_info),
)
