from django.contrib import admin

from .models import Listings, Comments, Watchlist, Categories, Bids
# Register your models here.
class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing",)

admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Categories)
admin.site.register(Bids)