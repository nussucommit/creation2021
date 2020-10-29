from django.urls import path

from . import views

urlpatterns = [
    path("", views.submit, name="submit"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # Kyknya register/ gaperlu di add, krn udah ada path dari main app (creation)
]
