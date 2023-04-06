from django.urls import path
from .views import PetView, PetsView

urlpatterns = [
    path("pets/", PetsView.as_view()),
    path("pets/<int:pet_id>/", PetView.as_view()),
]
