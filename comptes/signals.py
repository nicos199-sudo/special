from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Client

def client_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='client')
		instance.groups.add(group)
		Client.objects.create(
			user=instance,
			nom=instance.username,
			)
		print('Profile cree!')

post_save.connect(client_profile, sender=User)