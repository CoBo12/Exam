from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('addQuote', views.addQuote),
    path('like/<int:idquote>', views.like),
    path('logout', views.logout),
    path('user/<int:iduser>', views.userQuotes),
    path('edit', views.edit),
    path('updateaccount', views.updateaccount),
    path('delete/<int:idquote>', views.delete)
]