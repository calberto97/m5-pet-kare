from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import SexChoices


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=1)
    sex = serializers.ChoiceField(choices=SexChoices.choices, required=False)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
