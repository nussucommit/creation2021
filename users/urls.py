from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.submit, name="submit"),
    path("submit/<int:pk>/", views.form, name='submitdetail'),
]
