from django.db import models

#TODO: work out how to implement images
# store actual image in table or link to file?
class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ';')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)

class ArticleType(models.Model):
    type = models.CharField(max_length=30)

    def __unicode__(self):
        return self.type

class UserType(models.Model):
    type = models.CharField(max_length=30)

    def __unicode__(self):
        return self.type

class User(models.Model):
    userType = models.ForeignKey(UserType)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    email = models.EmailField()
 #  avatar = models.ImageField(upload_to='/tmp')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Certificate(models.Model):
    certificate = models.CharField(max_length=3)

    def __unicode__(self):
        return self.certificate

class DiscType(models.Model):
    format = models.CharField(max_length=1)
    description = models.CharField(max_length=10)

    def __unicode__(self):
        return self.description

class DVD(models.Model):
    title = models.CharField(max_length=100)
    purchase_date = models.DateField()
    dub_languages = models.CharField(max_length=100)
    subtitle_languages = models.CharField(max_length=100)
    special_features = SeparatedValuesField()
    disc_format = models.ForeignKey(DiscType)
    related_film = models.ForeignKey('Film')

    def __unicode__(self):
        return self.title

class Film(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    film_cast = models.CharField(max_length=300)
    director = models.CharField(max_length=100)
    duration = models.SmallIntegerField()
    certificate = models.ForeignKey(Certificate)
    release_date = models.DateField(blank=True)
    producer = models.CharField(max_length=200)
    distributor = models.CharField(max_length=50)
    website = models.CharField(max_length=100, blank=True)
    advice = models.CharField(max_length=100, blank=True)
    related_dvd = models.ForeignKey(DVD, null=True, blank=True)
    synopsis = models.CharField(max_length=300)
    thumbnail = models.CharField(max_length=100)
    still = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

#
# Manager subclasses for the different article types
#
class ReviewArticleManager(models.Manager):
    def get_query_set(self):
        return super(ReviewArticleManager, self).get_query_set().filter(article_type=1)

class InterviewArticleManager(models.Manager):
    def get_query_set(self):
        return super(InterviewArticleManager, self).get_query_set().filter(article_type=2)

class CompetitionArticleManager(models.Manager):
    def get_query_set(self):
        return super(CompetitionArticleManager, self).get_query_set().filter(article_type=3)

class NewsArticleManager(models.Manager):
    def get_query_set(self):
        return super(NewsArticleManager, self).get_query_set().filter(article_type=4)

class DVDArticleManager(models.Manager):
    def get_query_set(self):
        return super(DVDArticleManager, self).get_query_set().filter(article_type=5)

class Article(models.Model):
    article_type = models.ForeignKey(ArticleType)
    author = models.ForeignKey(User)
    headline = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    rating = models.SmallIntegerField()
    related_film = models.ForeignKey(Film)
    pub_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title

    objects = models.Manager() # The default manager.
    reviews = ReviewArticleManager()
    interviews = InterviewArticleManager()
    competitions = CompetitionArticleManager()
    news = NewsArticleManager()
    dvds = DVDArticleManager()

class ArticleDetailType(models.Model):
    article_type = models.ForeignKey(ArticleType)
    detail_type = models.CharField(max_length=30)

    def __unicode__(self):
        return self.detail_type

class ArticleDetail(models.Model):
    article = models.ForeignKey(Article)
    detail_type = models.ForeignKey(ArticleDetailType)
    detail = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s %s %s' % (self.article, self.detail_type, self.detail)

