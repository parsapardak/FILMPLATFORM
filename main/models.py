from django.db import models
from django.contrib.auth.models import User  # برای User پیش‌فرض Django




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



from django.contrib.auth.models import User

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ارتباط با کاربر
    movie = models.ForeignKey('MoviesSeries', on_delete=models.CASCADE)  # ارتباط با فیلم
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # جلوگیری از تکرار یک فیلم در واچ لیست کاربر

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"



    
from django.contrib.auth.models import User
from django.db import models

class Subscription(models.Model):
    TYPE_CHOICES = [
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Free')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"





    