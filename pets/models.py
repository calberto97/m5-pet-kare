from django.db import models


class Pet(models.Model):
    class SexChoices(models.TextChoices):
        MALE = "Male"
        FEMALE = "Female"
        NOT_INFORMED = "Not Informed"

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    sex = models.CharField(
        max_length=20,
        choices=SexChoices.choices,
        default=SexChoices.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
    ...
