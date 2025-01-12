from django.contrib import admin
from .models import MoviesSeries, Genre, Actor, Director, Review, Subscription, Watchlist, Subscription

@admin.register(MoviesSeries)
class MoviesSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'popularity', 'average_rating', 'download_link')
    list_filter = ('genres', 'release_date')
    search_fields = ('title',)
    def get_director(self, obj):
        return obj.director.name if obj.director else "No Director"
    get_director.short_description = 'Director'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('movies',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'birth_date', 'nationality')
    search_fields = ('name', 'nationality')  # جستجو
    list_filter = ('birth_date', 'nationality')  # فیلتر
    exclude = ('moviesseries',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('moviesseries',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')
    list_filter = ('rating',)
    search_fields = ('comment',)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie')
    search_fields = ('user__username', 'movie__title')


from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Subscription

# تنظیم Subscription در پنل ادمین
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'start_date', 'end_date', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username',)

# افزودن قابلیت نمایش اشتراک در صفحه کاربر
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    def subscription_type(self, obj):
        try:
            return obj.subscription.type
        except Subscription.DoesNotExist:
            return "No Subscription"
    subscription_type.short_description = 'Subscription Type'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
