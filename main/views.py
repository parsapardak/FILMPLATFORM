from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MovieForm,GenreForm, ActorForm, DirectorForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login




@login_required
@user_passes_test(lambda u: u.is_staff)  # فقط برای ادمین‌ها
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # بعداً URL صفحه اصلی رو مشخص می‌کنیم
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})




@login_required
@user_passes_test(lambda u: u.is_staff)  # فقط برای ادمین‌ها
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # به صفحه اصلی یا صفحه مورد نظر منتقل شود
    else:
        form = GenreForm()
    return render(request, 'main/add_genre.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_staff)
def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ActorForm()
    return render(request, 'main/add_actor.html', {'form': form})





@login_required
@user_passes_test(lambda u: u.is_staff)
def add_director(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DirectorForm()
    return render(request, 'main/add_director.html', {'form': form})



def home(request):
    # فیلم‌های پیشنهادی: جدیدترین ۶ فیلم
    recommended_movies = MoviesSeries.objects.order_by('-release_date')[:6]
    return render(request, 'main/home.html', {'movies': recommended_movies})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ورود خودکار بعد از ثبت‌نام
            return redirect('home')  # هدایت به صفحه اصلی
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

from django.contrib.auth.decorators import login_required, user_passes_test




#ویو لیست فیلم
from .models import MoviesSeries
def movie_list(request):
    movies = MoviesSeries.objects.all()
    return render(request, 'main/movie_list.html', {'movies': movies})


from django.db.models import Avg
from .models import MoviesSeries
def movie_list(request):
    sort_by = request.GET.get('sort_by', 'title')  # دریافت فیلتر از پارامتر URL
    if sort_by == 'rating':
        movies = MoviesSeries.objects.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')
    elif sort_by == 'release_date':
        movies = MoviesSeries.objects.order_by('-release_date')
    elif sort_by == 'popularity':
        movies = MoviesSeries.objects.order_by('-popularity')
    else:
        movies = MoviesSeries.objects.order_by('title')  # مرتب‌سازی پیش‌فرض
    return render(request, 'main/movie_list.html', {'movies': movies, 'sort_by': sort_by})




#  ویو هر فیلم بعد از تغییر برای کاربرای پریمیوم
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MoviesSeries

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(MoviesSeries, id=movie_id)
    user_subscription = getattr(request.user, 'subscription', None)
    can_download = user_subscription and user_subscription.type == 'Premium'
    return render(request, 'main/movie_detail.html', {
        'movie': movie,
        'can_download': can_download
    })





#ویو لیست بازیگران
from .models import Actor
def actor_list(request):
    actors = Actor.objects.all()
    return render(request, 'main/actor_list.html', {'actors': actors})



from django.db.models import Count, Avg
from .models import Actor
def actor_list(request):
    sort_by = request.GET.get('sort_by', 'name')  # دریافت فیلتر از پارامتر URL
    if sort_by == 'movies_count':
        actors = Actor.objects.annotate(movies_count=Count('moviesseries')).order_by('-movies_count')
    elif sort_by == 'popularity':
        actors = Actor.objects.annotate(popularity=Avg('moviesseries__popularity')).order_by('-popularity')
    else:
        actors = Actor.objects.order_by('name')  # مرتب‌سازی پیش‌فرض
    return render(request, 'main/actor_list.html', {'actors': actors, 'sort_by': sort_by})



#ویو هر بازیگر
def actor_detail(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    return render(request, 'main/actor_detail.html', {'actor': actor})



#واچ لیست
from django.shortcuts import render, redirect, get_object_or_404
from .models import Watchlist, MoviesSeries
from django.contrib.auth.decorators import login_required

@login_required
def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    return render(request, 'main/watchlist.html', {'watchlist': watchlist})

@login_required
def add_to_watchlist(request, movie_id):
    # بررسی وجود فیلم در پایگاه داده
    movie = get_object_or_404(MoviesSeries, id=movie_id)
    
    # ایجاد واچ لیست در صورت عدم وجود
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    
    # اضافه کردن فیلم به واچ لیست
    watchlist.movies.add(movie)
    
    return redirect('watchlist')

@login_required
def remove_from_watchlist(request, movie_id):
    movie = MoviesSeries.objects.get(id=movie_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.movies.remove(movie)
    return redirect('watchlist')



#صفحه کاربر
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    watchlist = request.user.watchlist_set.all()  # واچ لیست کاربر
    return render(request, 'main/user_profile.html', {'watchlist': watchlist})
@login_required
def user_profile(request):
    subscription = request.user.subscription if hasattr(request.user, 'subscription') else None
    return render(request, 'main/user_profile.html', {
        'user': request.user,
        'subscription': subscription,
    })




#گزارش ها
from django.db.models import Count
from .models import MoviesSeries, Actor, Genre

def reports(request):
    # پربازدیدترین فیلم‌ها
    top_movies = MoviesSeries.objects.order_by('-popularity')[:5]

    # بازیگرانی که در بیشترین فیلم‌ها حضور دارند
    top_actors = Actor.objects.annotate(movie_count=Count('moviesseries')).order_by('-movie_count')[:5]

    # ژانرهای محبوب
    top_genres = Genre.objects.annotate(movie_count=Count('movies')).order_by('-movie_count')[:5]

    return render(request, 'main/reports.html', {
        'top_movies': top_movies,
        'top_actors': top_actors,
        'top_genres': top_genres,
    })


#لاگ اوووت
from django.shortcuts import render

def logout_confirmation(request):
    return render(request, 'registration/logout_confirmation.html')




#جست و جو
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '')  # دریافت متن جستجو
    movie_results = MoviesSeries.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    actor_results = Actor.objects.filter(name__icontains=query)
    genre_results = Genre.objects.filter(name__icontains=query)

    return render(request, 'main/search_results.html', {
        'query': query,
        'movie_results': movie_results,
        'actor_results': actor_results,
        'genre_results': genre_results,
    })



#ادمین ****
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Watchlist

@login_required
def user_profile(request):
    watchlist = Watchlist.objects.filter(user=request.user)  # واچ لیست کاربر

    return render(request, 'main/user_profile.html', {
        'user': request.user,
        'watchlist': watchlist,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_profile(request):
    return render(request, 'main/user_profile.html', {'user': request.user})


from django.contrib.auth.models import User
from .models import Subscription
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)  # فقط برای سوپریوزر
def change_subscription(request, user_id, new_type):
    user = get_object_or_404(User, id=user_id)
    subscription, created = Subscription.objects.get_or_create(user=user)
    subscription.type = new_type
    subscription.save()
    return redirect('user_list')  # بازگشت به لیست کاربران


from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        subscription_type = user.subscription.type if hasattr(user, 'subscription') else "Free"
        user_data.append({
            'username': user.username,
            'email': user.email,
            'subscription': subscription_type,
            'id': user.id,
        })
    return render(request, 'main/user_list.html', {'users': user_data})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Subscription

# لیست کاربران برای مدیریت توسط سوپریوزر
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    users = User.objects.all()
    user_data = []

    for user in users:
        # بررسی وجود اشتراک برای کاربر
        subscription = Subscription.objects.filter(user=user).first()
        subscription_type = subscription.type if subscription else "Free"
        status = "Active" if user.is_active else "Inactive"

        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'subscription': subscription_type,
            'status': status,
        })

    return render(request, 'main/manage_users.html', {'users': user_data})

# تغییر اشتراک کاربر
@user_passes_test(lambda u: u.is_superuser)
def change_subscription(request, user_id, new_type):
    user = get_object_or_404(User, id=user_id)

    # ایجاد اشتراک در صورت عدم وجود
    subscription, created = Subscription.objects.get_or_create(user=user)
    subscription.type = new_type
    subscription.save()

    return redirect('manage_users')
