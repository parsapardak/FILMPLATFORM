from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import MoviesSeries, Genre, Actor, Director, Review, Subscription, Watchlist


# تنظیمات MoviesSeries
@admin.register(MoviesSeries)
class MoviesSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'popularity', 'average_rating', 'download_link')
    list_filter = ('genres', 'release_date')
    search_fields = ('title',)
    filter_horizontal = ('genres', 'actors')  # فیلتر چندتایی برای ژانرها و بازیگران
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'release_date', 'poster', 'download_link'),
        }),
        ('Additional Information', {
            'fields': ('genres', 'actors', 'director', 'popularity', 'average_rating', 'is_series'),
        }),
    )


# تنظیمات Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# تنظیمات Actor
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'nationality')
    search_fields = ('name', 'nationality')
    list_filter = ('birth_date', 'nationality')
    exclude = ('moviesseries',)


# تنظیمات Director
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality')
    search_fields = ('name', 'nationality')


# تنظیمات Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_date')
    list_filter = ('rating', 'created_date')
    search_fields = ('comment',)


# تنظیمات Watchlist
from django.contrib import admin
from .models import Watchlist, MoviesSeries

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_movies', 'created_at')  # اضافه کردن ستون‌های مورد نیاز
    search_fields = ('user__username', 'movies__title')  # جستجو بر اساس نام کاربر و عنوان فیلم
    filter_horizontal = ('movies',)  # فعال‌سازی رابط کاربری برای فیلتر کردن فیلم‌ها در واچ لیست

    def display_movies(self, obj):
        """نمایش لیست فیلم‌ها به صورت خلاصه"""
        return ", ".join([movie.title for movie in obj.movies.all()])
    display_movies.short_description = 'Movies in Watchlist'


# تنظیم Subscription در پنل مدیریت
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'start_date', 'end_date', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username',)


# افزودن قابلیت نمایش اشتراک در صفحه کاربر
class SubscriptionInline(admin.StackedInline):
    model = Subscription
    can_delete = False
    verbose_name_plural = 'Subscription'


class CustomUserAdmin(UserAdmin):
    inlines = (SubscriptionInline,)
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login', 'subscription_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    def subscription_status(self, obj):
        return obj.subscription.type if hasattr(obj, 'subscription') else "No Subscription"
    subscription_status.short_description = 'Subscription'


# ثبت User با تنظیمات جدید
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
