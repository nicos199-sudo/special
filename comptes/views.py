from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .forms import CommandeForm, CreateUserForm, ClientForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from .models import *
from .filters import CommandeFilter

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		
	context = {'form':form}
	return render(request, 'comptes/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'comptes/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def acceuil(request):
   commandes = Commande.objects.all()
   clients = Client.objects.all()

   total_clients = clients.count()

   total_commandes = commandes.count()
   livree = commandes.filter(status='Livree').count()
   en_attente = commandes.filter(status='En attente').count()

   context = {'commandes':commandes, 'clients':clients,
   'total_commandes':total_commandes,'livree':livree,
   'en_attente':en_attente }

   return render(request, 'comptes/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def userPage(request):
	commandes = request.user.client.commande_set.all()

	total_commandes = commandes.count()
	livree = commandes.filter(status='livree').count()
	en_attente = commandes.filter(status='en_attente').count()

	print('COMMANDES:', commandes)

	context = {'commandes':commandes, 'total_commandes':total_commandes,
	'livree':livree,'en_attente':en_attente}
	return render(request, 'comptes/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def accountSettings(request):
	client = request.user.client
	form = ClientForm(instance=client)

	if request.method == 'POST':
		form = ClientForm(request.POST, request.FILES,instance=client)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'comptes/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def produit(request):
    produits = Produit.objects.all()
    return render(request, 'comptes/produit.html', {'produits':produits})
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def client(request, pk_test):
    client = Client.objects.get(id=pk_test)

    commandes = client.commande_set.all()
    commande_count = commandes.count()
    myFilter = CommandeFilter(request.GET, queryset=commandes)
    commandes = myFilter.qs
    context = {'client':client, 'commandes':commandes, 'commande_count':commande_count, 'myFilter':myFilter}
    return render(request, 'comptes/client.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])   
def createCommande(request, pk):
    CommandeFormSet = inlineformset_factory(Client, Commande, fields=('produit', 'status'), extra=10 )
    client = Client.objects.get(id=pk)
    formset = CommandeFormSet(queryset=Commande.objects.none(),instance=client)
    #form = OrderForm(initial={'client':client})
    if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
	    formset = CommandeFormSet(request.POST, instance=client)
	    if formset.is_valid():
		    formset.save()
		    return redirect('/')

    context = {'form':formset}
    return render(request, 'comptes/commande_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCommande(request, pk):

	commande = Commande.objects.get(id=pk)
	form = CommandeForm(instance=commande)

	if request.method == 'POST':
		form = CommandeForm(request.POST, instance=commande)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'comptes/commande_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCommande(request, pk):
	commande = Commande.objects.get(id=pk)
	if request.method == "POST":
		commande.delete()
		return redirect('/')

	context = {'item':commande}
	return render(request, 'comptes/delete.html', context)