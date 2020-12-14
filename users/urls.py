from django.urls import path

from . import views

urlpatterns = [
    path("", views.submit, name="submit"),
    path("1/", views.form_1, name='1'),
    path("2/", views.form_2, name='2'),
    path("3/", views.form_3, name='3')
]
