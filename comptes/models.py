from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Client(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	nom = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_creation = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.nom


class Tag(models.Model):
	nom = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.nom

class Produit(models.Model):
	CATEGORY = (
			('Interieur', 'Interieur'),
			('Exterieur', 'Exterieur'),
			) 

	nom = models.CharField(max_length=200, null=True)
	prix = models.FloatField(null=True)
	categorie = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_creation = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.nom




class Commande(models.Model):
	STATUS = (
			('En attente', 'En attente'),
			('En cours de livraison', 'En cours de livraison'),
			('Livree', 'Livree'),
			)

	client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
	produit = models.ForeignKey(Produit, null=True, on_delete= models.SET_NULL)
	date_creation = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
    		return self.produit.nom

	


	
