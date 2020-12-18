from django.urls import path

from . import views
from users.views import submit, register

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name="faq"),
    path('rules', views.rules, name="rules"),
    path('timeline', views.timeline, name="timeline"),
    path('legacy', views.legacy, name="legacy"),
    path('challenge', views.challenge, name="challenge"),
    path('registration', register, name="registration"),    #register imported from users/views.py
    path('submission', submit, name="submission"),  # submit imported from users/views.py
    path('contact', views.contact, name="contact"),
    path('user', views.user, name="user"),
    path('challenge1', views.challenge_statement_1, name="statement1"),
    path('challenge2', views.challenge_statement_2, name="statement2"),
    path('challenge3', views.challenge_statement_3, name="statement3")
]