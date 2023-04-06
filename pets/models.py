from django.db import models


class SexChoices(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    sex = models.CharField(
        max_length=20,
        choices=SexChoices.choices,
        default=SexChoices.NOT_INFORMED,
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )

    def __repr__(self) -> str:
        return f"<Pet ({self.id} - {self.name})>"
