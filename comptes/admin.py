from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Tag)
admin.site.register(Commande)
