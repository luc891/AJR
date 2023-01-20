import json
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, UserForm, Game, GameForm, ContactForm, NewsForm, News

# Define local time as France
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def index(request):

    # When creating a news
    if request.method == 'POST':
        form = NewsForm(request.POST)

        # If form is valid, create new News object and display index page
        if form.is_valid():
            news = News(user = request.user,
                        text = request.POST['text'])
            news.save()
            news = News.objects.all()
            return render(request, 'index.html', {
                'news': news
            })
        
    # When just displaying index page
    else:
        news = News.objects.all()
        return render(request, 'index.html', {
            'news': news
        })


def register(request):

    # Display registration form
    if request.method == 'GET':
        return render(request, 'register.html')
    
    # Record new user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'],
                                            email = form.cleaned_data['username'],
                                            first_name = form.cleaned_data['first_name'],
                                            last_name = form.cleaned_data['last_name'],
                                            phone = form.cleaned_data['phone'],
                                            adress = form.cleaned_data['adress'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        # If informations provided are not valid, display error message 
        else:
            message = "Informations non valides"
            return render(request, 'register.html', {
                'alert' : message
            })

@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def loginview(request):

    # After clicking login button
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # If authentication successful
        if user :
            login(request, user)
            return HttpResponseRedirect(reverse("profil"))
        else:
            return render(request, "login.html", {
                "message": "Email et/ou Mot de passe invalide."
            })
    # Display login page
    else:
        return render(request, "login.html")


@login_required
def profil(request):

    # When user records a new game
    if request.method == 'POST':
        game = GameForm(request.POST, request.FILES)
        if game.is_valid():
            game.save()
            return HttpResponseRedirect(reverse('catalog'))

    # Display the user profil page
    else:

        # Get the list of categories of games in case user wants to add a game
        genres = []
        for g in Game.genre.field.choices:
            genres.append(g[0])

        # Retrieve a list of all games added by user
        games = Game.objects.filter(owner = request.user)

        return render(request, "profil.html", {
            'games' : games,
            'genres': genres
        })

# Display a list of all available games
def catalog(request):
    games = Game.objects.all()

    # Get a list with all the categories
    categories = []
    for g in Game.genre.field.choices:
        categories.append(g[0])

    # Range of age the user will be able to use to filter displayed games
    age_min = range(3, 17)
    return render(request, "catalog.html", {
        'games': games,
        'categories': categories,
        'age_min': age_min
    })

# Display details of a game
def game(request, title):
    game = Game.objects.get(title = title)
    return render(request, "game.html", {
        'game': game,
    })


def contact(request):

    # When a message is sent
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            # Message details
            subject = 'Contact depuis le site web'
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, sender, [""]) # Receiver email adress
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return render(request, "contact.html", {
                'message': 'Email bien envoyé !'
            })
        
    # Display contact page, passes the current user to template
    # to display their email adress in the 'from' field
    else:
        form = ContactForm()
        return render(request, "contact.html", {
            'form': form,
            'user': request.user
        })

# User details modification
@login_required
def modify(request):
    if request.method == 'POST':
        user = User.objects.get(pk = request.user.id)

        # If user info are updated
        if 'informations' in request.POST :            
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone = request.POST['phone']
            user.adress = request.POST['adress']
            user.save()

        # If password is changed by user
        if 'password' in request.POST :
            if request.POST['password1'] == request.POST['password2']:
                user.set_password(request.POST['password1'])
                user.save()
                messages.success(request, 'Mot de passe modifié')
                login(request, user)
            
        return HttpResponseRedirect(reverse("profil"))

# Remove game from catalog
def remove(request):
    if request.method == 'POST':
        title = json.loads(request.body)['title']
        game = Game.objects.get(title = title)
        game.delete()

    return JsonResponse(status = 200)

# Modify game details
def modify_game(request, title):

    # Display the game form, pre-filled by existing details
    if request.method == 'GET':
        game = Game.objects.get(title = title)
        genres = []
        for g in Game.genre.field.choices:
            genres.append(g[0])
        return render(request, 'modify_game.html', {
            'game': game,
            'genres' : genres
        })
    
    # Delete old version of game and recreates it with new details
    if request.method == 'POST':
        game = Game.objects.get(title=title)
        game.delete()
        game = GameForm(request.POST, request.FILES)
        if game.is_valid():
            game.save()
            return HttpResponseRedirect(reverse('catalog'))

# When a user wants to request a game for the next meeting
def game_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Message details
        subject = data['subject']
        sender = request.user.username
        message = 'Pour la prochaine réunion de l\'association, le jeu ' + data['body']['game'] + ' a été demandé par ' + data['body']['user']
        try:
            send_mail(subject, message, sender, [""]) # Receiver email adress
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        
        return JsonResponse({'message' : 'Tout est ok'}, status = 200)