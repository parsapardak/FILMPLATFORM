from django import forms
from .models import MoviesSeries, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = MoviesSeries
        fields = ['title', 'description', 'release_date', 'poster', 'genres', 'actors', 'director']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'movie', 'rating', 'comment']
from .models import Genre, Actor, Director

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name']

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name']
