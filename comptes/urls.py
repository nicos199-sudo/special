from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('compte/', views.accountSettings, name="compte"),
    path('', views.acceuil, name='home'),
    
    path('produit/', views.produit, name='produit'),
    path('client/<str:pk_test>/', views.client, name='client'),
    path('creer_commande/<str:pk>/', views.createCommande, name='creer_commande'),
    path('modifier_commande/<str:pk>/', views.updateCommande, name='modifier_commande'),
    path('supprimer_commande/<str:pk>/', views.deleteCommande, name='supprimer_commande'),

    
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="comptes/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="comptes/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="comptes/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="comptes/password_reset_done.html"), 
        name="password_reset_complete"),
]