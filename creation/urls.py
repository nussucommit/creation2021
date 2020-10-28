from django.urls import path

from . import views
from users.views import submit

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name="faq"),
    path('rules', views.rules, name="rules"),
    path('timeline', views.timeline, name="timeline"),
    path('legacy', views.legacy, name="legacy"),
    path('challenge', views.challenge, name="challenge"),
    path('registration', views.registration, name="registration"),
    path('submission', submit, name="submission"),  # submit imported from users/views.py
    path('contact', views.contact, name="contact"),
]