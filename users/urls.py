from django.urls import path
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

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
    path('challenge5', views.side_challenge, name="sidechallenge"),
    path('signup1', views.signup_statement_1, name="signup1"),
    path('signup2', views.signup_statement_2, name="signup2"),
    path('signup3', views.signup_statement_3, name="signup3"),
    path('signup4', views.signup_statement_4, name="signup4"),
    path('signupside', views.signup_side_statement, name="signupside"),
    path('profile', views.profile, name='profile'),
    path('inquiries',views.inquiries, name="inquiries"),
    path('thankyou',views.thankyou, name="thankyou")
]

urlpatterns += [
    path("submit/", views.submit, name="submit"),
    path("submit/<int:pk>/", views.form, name='submitdetail'),
]

