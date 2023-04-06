from django.core.serializers import serialize
from django.db.migrations import serializer
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pet
from groups.models import Group
from pets.serializers import PetSerializer
from traits.models import Trait


class PetsView(APIView, PageNumberPagination):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        try:
            group_db = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group_db = Group.objects.create(**request.data["group"])

        pet = Pet.objects.create(**serializer.validated_data, group=group_db)

        trait_db = []
        for trait in traits_data:
            try:
                trait_db = Trait.objects.get(name__iexact=trait["name"])
            except Trait.DoesNotExist:
                trait_db = Trait.objects.create(**trait)
            pet.traits.add(trait_db)

        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=201)

    def get(self, request):
        trait = request.query_params.get("trait")

        if trait:
            pets = Pet.objects.filter(traits__name__iexact=trait)

        else:
            pets = Pet.objects.all()

        pages = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)


class PetView(APIView):
    def get(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, 200)

    def delete(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()
        return Response(status=204)

    def patch(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                group_db = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group_db = Group.objects.create(**request.data["group"])
            pet.group = group_db

        if traits_data:
            pet.traits.clear()
            for trait in traits_data:
                try:
                    trait_db = Trait.objects.get(name__iexact=trait["name"])
                except Trait.DoesNotExist:
                    trait_db = Trait.objects.create(**trait)
                pet.traits.add(trait_db)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, 200)
