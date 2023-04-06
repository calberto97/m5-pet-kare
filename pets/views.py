from django.forms.models import model_to_dict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pet
from groups.models import Group
from pets.serializers import PetSerializer
from traits.models import Trait


class PetView(APIView, PageNumberPagination):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        try:
            group_db = Group.objects.get(
                scientific_name__icontains=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group_db = Group.objects.create(**request.data["group"])

        pet = Pet.objects.create(**serializer.validated_data, group=group_db)

        trait_db = []
        for trait in traits_data:
            try:
                trait_db = Trait.objects.get(name__icontains=trait["name"])
            except Trait.DoesNotExist:
                trait_db = Trait.objects.create(**trait)
            pet.traits.add(trait_db)

        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=201)

    def get(self, request):
        pets = Pet.objects.all()
        pages = self.paginate_queryset(pets, request, view=self)
        # pets_dict = [model_to_dict(p) for p in pets]
        # return Response(pets_dict)
        serializer = PetSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)
        ...
