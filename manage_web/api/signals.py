# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import Review

# @receiver(post_save, sender=Review)
# def create_image_(sender, instance, **kwargs):
#     id = instance.id
#     image = instance.image
#     URL = str(instance.registered_nuc.ip)
#     data = {
#         'id': id,
#         'image': image
#     } 
#     res = requests.post(URL, data=data)


