from django.conf.urls.defaults import *
from django.views.generic import list_detail
from eiga.models import Article
from eiga import views
from django.conf import settings
from datetime import datetime, timedelta
incinema_date_range = datetime.today() - timedelta(days=42)

from django.contrib import admin
admin.autodiscover()

#incinemas_list_info = {
#    'queryset': Article.reviews.filter(related_film__release_date__lte=datetime.now()).filter(related_film__release_date__gte=incinema_date_range).order_by('-related_film__release_date'),
#    "template_name" : "eiga/review_list.html",
#    "template_object_name" : "review",
#}

incinemas_list_info = {
    'queryset': Article.reviews.order_by('-related_film__release_date')[:5],
    "template_name" : "eiga/review_list.html",
    "template_object_name" : "review",
}

comingsoon_list_info = {
    'queryset': Article.reviews.filter(related_film__release_date__gte=datetime.now()).order_by('-related_film__release_date'),
    "template_name" : "eiga/review_list.html",
    "template_object_name" : "review",
}

outtobuy_list_info = {
    'queryset': Article.dvds.order_by('-related_film__release_date'),
    "template_name" : "eiga/outtobuy_list.html",
    "template_object_name" : "review",
}

review_detail_info = {
    'queryset': Article.objects.all(),
    "template_name" : "eiga/review_detail.html",
    "template_object_name" : "review",
}

##interview_list_info = {
##    'queryset': Article.interviews.all(),
##    "template_name" : "eiga/interview_list.html",
##    "template_object_name" : "interview",
##}
##
##interview_detail_info = {
##    'queryset': Article.interviews.all(),
##    "template_name" : "eiga/interview_detail.html",
##    "template_object_name" : "interview",
##}
##
##news_list_info = {
##    'queryset': Article.news.all(),
##    "template_name" : "eiga/news_list.html",
##    "template_object_name" : "news",
##}
##
##news_detail_info = {
##    'queryset': Article.news.all(),
##    "template_name" : "eiga/news_detail.html",
##    "template_object_name" : "news",
##}
##
##competition_list_info = {
##    'queryset': Article.competitions.all(),
##    "template_name" : "eiga/competition_list.html",
##    "template_object_name" : "competition",
##}
##
##competition_detail_info = {
##    'queryset': Article.competitions.all(),
##    "template_name" : "eiga/competition_detail.html",
##    "template_object_name" : "competition",
##}

urlpatterns = patterns('',
    (r'^home/$', views.home),
    (r'^incinemas/$', list_detail.object_list, incinemas_list_info),
    (r'^comingsoon/$', list_detail.object_list, comingsoon_list_info),
    (r'^outtobuy/$', list_detail.object_list, outtobuy_list_info),
    (r'^outtobuy/(?P<object_id>\d+)/$', views.outtobuy_detail),
    (r'^reviewarchive/$', views.archive_listing),
    (r'^reviews/(?P<object_id>\d+)/$', list_detail.object_detail, review_detail_info),

   # (r'^interviews/$', list_detail.object_list, interview_list_info),
   # (r'^interviews/(?P<object_id>\d+)/$', list_detail.object_detail, interview_detail_info),
   # (r'^news/$', list_detail.object_list, news_list_info),
   # (r'^news/(?P<object_id>\d+)/$', list_detail.object_detail, news_detail_info),
   # (r'^competitions/$', list_detail.object_list, competition_list_info),
   # (r'^competitions/(?P<object_id>\d+)/$', list_detail.object_detail, competition_detail_info),

)