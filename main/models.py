from django.db import models
from django.contrib.auth.models import User  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class MoviesSeries(models.Model):
    title = models.CharField(max_length=200)  # عنوان
    description = models.TextField(blank=True, null=True)  # توضیحات
    release_date = models.DateField(blank=True, null=True)  # تاریخ انتشار
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)  # پوستر
    genres = models.ManyToManyField('Genre', related_name='related_genres')  # اضافه کردن related_name یکتا
    actors = models.ManyToManyField('Actor', related_name='related_actors')  # اضافه کردن related_name یکتا
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, blank=True, related_name='directed_movies')  # کارگردان
    popularity = models.IntegerField(default=0)  # محبوبیت
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # میانگین امتیاز
    is_series = models.BooleanField(default=False)  # آیا سریال است یا خیر
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    download_link = models.URLField(max_length=500, blank=True, null=True)  # لینک دانلود فیلم
    likes = models.ManyToManyField(User, related_name='liked_movies', blank=True)  # تعریف فیلد لایک

    def __str__(self):
        return self.title




class Genre(models.Model):
    name = models.CharField(max_length=50)
    movies = models.ManyToManyField('MoviesSeries', related_name='genre_movies')  # اضافه کردن related_name یکتا

    def __str__(self):
        return self.name



class Actor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='actors/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    moviesseries = models.ManyToManyField('MoviesSeries', related_name='actor_movies')  # اضافه کردن related_name یکتا
    awards = models.TextField(blank=True, null=True)  # لیست جوایز


    def __str__(self):
        return self.name




class Director(models.Model):
    name = models.CharField(max_length=100)  # نام کارگردان
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # کاربر
    movie = models.ForeignKey(MoviesSeries, on_delete=models.CASCADE)  # فیلم
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # امتیاز
    comment = models.TextField(blank=True, null=True)  # نظر
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"





class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')  # هر کاربر یک واچ لیست دارد
    movies = models.ManyToManyField('MoviesSeries', related_name='in_watchlists')  # ارتباط چند به چند با فیلم‌ها
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد واچ لیست

    def __str__(self):
        return f"{self.user.username}'s Watchlist"


    


class Subscription(models.Model):
    TYPE_CHOICES = [
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='subscription')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Free')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

# ایجاد اشتراک پیش‌فرض برای کاربران جدید
@receiver(post_save, sender=User)
def create_subscription_for_new_user(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.get_or_create(user=instance, defaults={'type': 'Free'})





    