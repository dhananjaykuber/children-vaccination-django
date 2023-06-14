from .models import Children, Vaccine
from django.db.models.signals import post_save
from django.dispatch import receiver


# singal receiver for vaccine date updation
@receiver(post_save, sender=Children)
def update_vaccine_date(sender, instance, update_fields, **kwargs):
    if instance._state.adding:
        return

    try:
        old_instance = Children.objects.get(id=instance.id)
    except Children.DoesNotExist:
        return

    print(old_instance, update_fields)

    if old_instance.dob != instance.dob:
        vaccines = Vaccine.objects.filter(children=instance)

        print("hi")
