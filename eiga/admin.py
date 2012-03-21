from django.contrib import admin
from SMP.eiga.models import Article, ArticleType, Certificate, Film, DiscType, DVD, User, UserType, ArticleDetailType, ArticleDetail

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type', 'author', 'headline', 'rating')
    search_fields = (
        'title',
    )

class ArticleDetailTypeAdmin(admin.ModelAdmin):
    list_display = ('article_type', 'detail_type')

class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('article', 'detail_type', 'detail')

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate',)

class DVDAdmin(admin.ModelAdmin):
    list_display = ('title', 'purchase_date', 'dub_languages', 'subtitle_languages', 'special_features', 'disc_format')
    search_fields = (
         'title',
    )

class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'film_cast', 'director', 'duration', 'certificate', 'release_date', 'related_dvd')
    search_fields = (
         'title',
    )

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'userType', 'sex', 'email')

    def full_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name))
    full_name.short_description = 'Name'


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleType)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(DiscType)
admin.site.register(DVD, DVDAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserType)
admin.site.register(ArticleDetailType, ArticleDetailTypeAdmin)
admin.site.register(ArticleDetail, ArticleDetailAdmin)