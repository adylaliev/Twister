from django.contrib import admin

# Register your models here.
from twister.models import Publication, Comment, RatingStar, Rating, Likes, Favorites

admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Likes)
admin.site.register(Favorites)
