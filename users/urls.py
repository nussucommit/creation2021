from django.urls import path

from . import views

urlpatterns = [
    path("", views.submit, name="submit")
    # Kyknya register/ gaperlu di add, krn udah ada path dari main app (creation)
]
