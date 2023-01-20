from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logoutview, name="logout"),
    path("login", views.loginview, name="login"),
    path("register", views.register, name="register"),
    path("profil", views.profil, name="profil"),
    path("catalog", views.catalog, name="catalog"),
    path("game/<title>", views.game, name="game"),
    path("contact", views.contact, name="contact"),
    path("index", views.index, name="index"),
    path("modify", views.modify, name="modify"),
    path("remove", views.remove, name="remove"),
    path("modify_game/<title>", views.modify_game, name="modify_game"),
    path("game_request", views.game_request, name="game_request"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name = 'password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]