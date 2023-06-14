from django.db import models

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Children(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=100, default="")
    parent_email = models.EmailField()
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.parent_email


class Vaccine(models.Model):
    children = models.ForeignKey(Children, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date = models.DateField()
    vaccine_name = models.CharField(max_length=100, default="")
    taken = models.BooleanField(default=False)

    def __str__(self):
        return self.vaccine_name
