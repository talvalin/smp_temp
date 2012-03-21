from django.conf.urls.defaults import *
from eiga.models import Article

info_dict = {
    'queryset': Article.reviews.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
)
