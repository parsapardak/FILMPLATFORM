from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('add-genre/', views.add_genre, name='add_genre'),
    path('add-actor/', views.add_actor, name='add_actor'),
    path('add-director/', views.add_director, name='add_director'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('actors/', views.actor_list, name='actor_list'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add-to-watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('profile/', views.user_profile, name='user_profile'),  # مسیر پروفایل
    path('reports/', views.reports, name='reports'),
    path('search/', views.search, name='search'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user-list/', views.user_list, name='user_list'),
    path('change-subscription/<int:user_id>/<str:new_type>/', views.change_subscription, name='change_subscription'),

]
