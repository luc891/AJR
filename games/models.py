from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser


GAMES_TYPES = (
    ('Jeu de dés','dés'),
    ('Jeu d\'adresse','adresse'),
    ('Jeu d\'ambience', 'ambiance'),
    ('Jeu de cartes', 'cartes'),
    ('Jeu de plateau', 'plateau'),
    ('Jeu de mémoire', 'mémoire'),
    ('Jeu de connaissance', 'connaissance'),
    ('Jeu de lettres', 'lettres'),
    ('Jeu de logique', 'logique'),
    ('Jeu de pions', 'pions'),
    ('Jeu éducatif', 'éducatif'),
    ('Jeu d\'enquête', 'enquête'),
    ('Jeu de coopération', 'coopération'),
    ('Jeu de bluff', 'bluff'),
    ('Jeu de stratégie', 'stratégie'),
    ('Jeu de gestion', 'gestion'),
    ('Jeu de hasard', 'hasard'),
    ('Jeu de rôle', 'rôle'),
    ('Jeu créatif', 'créatif'),
)


class User(AbstractUser):
    phone = models.CharField(max_length = 10, blank = True)
    adress = models.CharField(max_length = 254, blank = True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Game(models.Model):
    title = models.CharField(max_length = 100)
    extension = models.BooleanField(default = False)
    min_players = models.IntegerField(default = 0)
    max_players = models.IntegerField(default = 99, blank = True)
    min_age = models.IntegerField(default = 0)
    duration = models.IntegerField(default = 60)
    description = models.TextField(blank = True)
    cover = models.ImageField(upload_to='media/covers/', default='media/covers/default_cover.jpeg')
    genre = models.CharField(max_length = 30, choices = GAMES_TYPES, default = 'Jeu de dés')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.title}'
        

class News(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add = True)
    text = models.TextField(blank = True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Actualité par {self.user}'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'phone', 'adress']


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'extension', 'min_players', 'max_players', 'min_age', 'duration', 'cover', 'description', 'genre', 'owner']


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['text']


class ContactForm(forms.Form):
    sender = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, required = True)