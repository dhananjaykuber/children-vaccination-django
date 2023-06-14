from rest_framework import serializers
from .models import Hospital, Children, Vaccine


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ["id", "name", "phone_number", "email", "password"]

    def create(self, validated_data):
        return Hospital.objects.create(**validated_data)


class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = [
            "id",
            "dob",
            "gender",
            "parent_name",
            "parent_email",
            "phone_number",
            "hospital",
        ]

    def create(self, validated_data):
        return Children.objects.create(**validated_data)


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ["id", "children", "hospital", "date", "vaccine_name", "taken"]

    def create(self, validated_data):
        return Vaccine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get("date", instance.date)
        instance.vaccine_name = validated_data.get(
            "vaccine_name", instance.vaccine_name
        )
        instance.taken = validated_data.get("taken", instance.taken)
        instance.save()
        return instance
