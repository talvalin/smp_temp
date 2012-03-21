from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.db.models import F
from itertools import chain
from django.template import RequestContext

from datetime import datetime, timedelta
incinema_date_range = datetime.today() - timedelta(days=42)

from eiga.models import Article

def home(request):
    incinema = Article.reviews.exclude(related_film__release_date=None).exclude(rating=9).order_by('-related_film__release_date')[:4]
    comingsoon = Article.reviews.exclude(related_film__release_date=None).exclude(rating=9)[:4]
    outtobuy = Article.reviews.exclude(related_film__release_date=None).filter(rating=5)[:4]
    #comingsoon = Article.reviews.filter(related_film__release_date__gte=datetime.now()).order_by('-related_film__release_date')[:3]
    #outtobuy = Article.dvds.order_by('-related_film__release_date')[:3]

    result_list = list(chain(incinema, comingsoon, outtobuy))

    return render_to_response('home.html', {'article_list': result_list}, context_instance=RequestContext(request))

def outtobuy_detail(request, object_id):
    # we've got an object_id for the DVD review, so in addition, return extra_content in the form
    # of all other review articles for that particular film
    review = Article.dvds.get(pk=object_id)
    related_review_list = Article.objects.filter(related_film=review.related_film).exclude(pk=object_id)

    review = {
        'dvd' : review,
        'related_review_list' : related_review_list,
    }

    return render_to_response('eiga/outtobuy_detail.html', {'review': review })

def archive_listing(request, page_size=50):
    review_list = Article.reviews.exclude(related_film__release_date=None).order_by('title')

    if page_size == -1:
        page_size = review_list.count()

    paginator = Paginator(review_list, page_size)

    page = int(request.GET.get('page', '1'))

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
         # If page is out of range, deliver last page of results.
        reviews = paginator.page(paginator.num_pages)

    return render_to_response('eiga/archive_list.html', {"reviews": reviews})

class InCinemasListView(ListView):
    context_object_name = "review_list"
    template_name = "eiga/review_list.html"

    def get_queryset(self):
        return Article.reviews.exclude(rating=9).order_by('-related_film__release_date')[:10]

class OutToBuyListView(ListView):
    context_object_name = "review_list"
    template_name = "eiga/outtobuy_list.html"

    def get_queryset(self):
        return Article.reviews.filter(related_film__related_dvd__isnull=False)

class ComingSoonListView(ListView):
    context_object_name = "review_list"
    template_name = "eiga/review_list.html"

    def get_queryset(self):
	    return Article.reviews.filter(related_film__release_date__gte=datetime(2011, 1, 1)).order_by('-related_film__release_date')[:10]