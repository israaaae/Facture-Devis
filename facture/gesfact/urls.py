from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('log', views.log, name='log'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('view_facture/<int:facture_id>/', views.view_facture, name='view_facture'),
    path('user_login/', views.user_login, name='user_login'),
    path('articles_list/', views.articles_list, name='articles_list'),
    path('clients_list/', views.clients_list, name='clients_list'),
    path('factures_list/', views.factures_list, name='factures_list'),
    path('create_article/', views.create_article, name='create_article'),
    path('create_facture/', views.create_facture, name='create_facture'),
    path('create_client/', views.create_client, name='create_client'),
    path('update_client/<int:client_id>/', views.update_client, name='update_client'),
    path('update_article/<int:article_id>/', views.update_article, name='update_article'),
    path('update_facture/<int:facture_id>/', views.update_facture, name='update_facture'),
    path('delete_facture/<int:facture_id>/', views.delete_facture, name='delete_facture'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),    
    path('delete_devis/<int:devis_id>/', views.delete_devis, name='delete_devis'),
    path('devis_list/', views.devis_list, name='devis_list'),
    path('update_devis/<int:devis_id>/', views.update_devis, name='update_devis'),
    path('create_devis/', views.create_devis, name='create_devis'),
    path('view_devis/<int:devis_id>/', views.view_devis, name='view_devis'),
    path('print_devis/<int:devis_id>/', views.print_devis, name='print_devis'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('generate_pdf/<int:facture_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('print_facture/<int:facture_id>/', views.print_facture, name='print_facture'),
    path('generate_pdf1/<int:devis_id>/pdf/', views.generate_pdf1, name='generate_pdf1'),
]

