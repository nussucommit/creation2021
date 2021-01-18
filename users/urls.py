from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name="faq"),
    path('rules', views.rules, name="rules"),
    path('timeline', views.timeline, name="timeline"),
    path('legacy', views.legacy, name="legacy"),
    path('challenge', views.challenge, name="challenge"),
    path('registration', views.register, name="registration"),  
    path('contact', views.contact, name="contact"),
    path('user', views.user, name="user"),
    path('challenge1', views.challenge_statement_1, name="statement1"),
    path('challenge2', views.challenge_statement_2, name="statement2"),
    path('challenge3', views.challenge_statement_3, name="statement3"),
    path('challenge4', views.challenge_statement_4, name="statement4"),
    path('challenge5', views.side_challenge, name="side challenge"),
    path('profile', views.profile, name='profile'),
]

urlpatterns += [
    path("submit/", views.submit, name="submit"),
    path("submit/<int:pk>/", views.form, name='submitdetail'),
]

