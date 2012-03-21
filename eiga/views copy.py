from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.db.models import F
import datetime

from eiga.models import Article

def home(request):
    article_list = Article.reviews.exclude(related_film__release_date=None).exclude(rating=9).order_by('-related_film__release_date')[:3]
    return render_to_response('home.html', {'article_list': article_list})

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

def archive_listing(request):
    review_list = Article.objects.order_by('title')
    paginator = Paginator(review_list, 50) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        reviews = paginator.page(page)
    except (EmptyPage, InvalidPage):
        reviews = paginator.page(paginator.num_pages)

    return render_to_response('eiga/archive_list.html', {"reviews": reviews})
