from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Client, Article, Devis, Facture, Profile
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from .forms import ClientForm, ArticleForm, DevisForm, FactureForm, LoginForm, AddProfileForm, LogForm
from django.db.models import Sum
from django.db.models import Sum, F
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Facture
from .models import Profile
from .models import Facture, Statistique  # Assurez-vous que vous avez importé le modèle Statistique
from .forms import AddProfileForm
from .forms import FactureForm  

def add_profile(request):
    if request.method == 'POST':
        form = AddProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['confirm_password']:
                messages.error(request, "Les mots de passe ne correspondent pas.")
            else:
                try:
                    # Créez le nouvel utilisateur et le profil ici
                    user = User.objects.create_user(
                        username=cd['employee_name'],
                        email=cd['email'],
                        password=cd['password']
                    )
                    profile = Profile.objects.create(
                        user=user,
                        email=cd['email'],
                        numero_telephone=cd['numero_telephone']
                    )

                    login(request, user)
                    messages.success(request, "Votre compte a été créé avec succès. Connectez-vous maintenant.")
                    return redirect('user_login')  # Redirige vers la page de connexion
                except:
                    messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
    else:
        form = AddProfileForm()
    return render(request, 'add_profile.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
                # Connexion réussie, redirigez vers la page souhaitée
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'form': form})



def home(request):
    return render(request, 'home.html')




def facture_template(request):
    return render(request, 'facture_template.html')






def log(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                log(request, user)
                return redirect('add_profile')
                # Connexion réussie, redirigez vers la page souhaitée
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LogForm()
    return render(request, 'log.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


def detail_client(request):
    return redirect('dashboard')



def clients_list(request):
    search_id = request.GET.get('search_id', '')
    search_name = request.GET.get('search_name', '')
    
    clients = Client.objects.all()
    
    if search_id:
        clients = clients.filter(identifiant__icontains=search_id)
    if search_name:
        clients = clients.filter(nom__icontains=search_name)
    
    context = {
        'clients': clients,
        'search_id': search_id,
        'search_name': search_name,
    }
    return render(request, 'clients_list.html', context)




def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')  # Redirigez vers la liste des clients après la création réussie
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})



def create_devis(request):
    if request.method == 'POST':
        form = DevisForm(request.POST)
        if form.is_valid():
            devis = form.save()
            return redirect('devis_list')
        else: 
            print(form.errors)
    else:
        form = DevisForm()
    return render(request, 'create_devis.html', {'form': form})



def create_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save()
            return redirect('factures_list')
        else: 
            print(form.errors)
    else:
        form = FactureForm()

    return render(request, 'create_facture.html', {'form': form})


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles_list')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})




def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'update_client.html', {'form': form, 'client': client})


def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles_list')
        else:
            print(form.errors)

    else:
        form = ArticleForm(instance=article)
    return render(request, 'update_article.html', {'form': form, 'article': article})


def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('clients_list')  # Rediriger vers la liste des factures après la suppression
    return render(request, 'delete_client.html', {'client': client})



def delete_devis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    if request.method == 'POST':
        devis.delete()
        return redirect('devis_list')  # Rediriger vers la liste des factures après la suppression
    return render(request, 'delete_devis.html', {'devis': devis})




def articles_list(request):
    search_id = request.GET.get('search_id', '')
    
    articles = Article.objects.all()
    
    if search_id:
        articles = articles.filter(reference__icontains=search_id)
    
    context = {
        'articles': articles,
        'search_id': search_id,
    }
    return render(request, 'articles_list.html', context)











def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('articles_list')  # Rediriger vers la liste des factures après la suppression
    return render(request, 'delete_article.html', {'article': article})




def devis_list(request):
    search_id = request.GET.get('search_id', '')
    
    deviss =  Devis.objects.all()
    
    if search_id:
        deviss = deviss.filter(numero_devis_icontains=search_id)
    
    context = {
        'deviss': deviss,
        'search_id': search_id,
    }
    return render(request, 'devis_list.html', context)






def update_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('factures_list')
    else:
        form = FactureForm(instance=facture)
    
    return render(request, 'update_facture.html', {'form': form, 'facture': facture})
 




def update_devis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    
    if request.method == 'POST':
        form = DevisForm(request.POST, instance=devis)
        if form.is_valid():
            form.save()
            return redirect('devis_list')
        else: 
            print(form.errors)
    else:
        form = DevisForm(instance=devis)
    
    return render(request, 'update_devis.html', {'form': form, 'devis': devis})








def factures_list(request):
    search_id = request.GET.get('search_id', '')
    
    factures = Facture.objects.all()
    
    if search_id:
        factures = factures.filter(numero_facture_icontains=search_id)
    
    context = {
        'factures': factures,
        'search_id': search_id,
    }
    return render(request, 'factures_list.html', context)





from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from .models import Facture, Devis

def print_facture(request, facture_id):
    # Obtenez l'objet Facture à partir de la base de données
    facture = get_object_or_404(Facture, pk=facture_id)

    # Chargez le modèle HTML de la facture
    template = get_template('facture_template.html')

    # Remplissez le modèle HTML avec les données de la facture
    context = {'facture': facture}
    html = template.render(context)

    # Créez un objet BytesIO pour stocker le PDF généré
    response = BytesIO()

    # Créez le PDF à partir du HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    # Vérifiez si la génération du PDF a réussi
    if not pdf.err:
        # Réponse avec le contenu PDF
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=facture_{facture.id}.pdf'

        # Ajoutez le script JavaScript pour déclencher l'impression automatiquement
        response.write('<script type="text/javascript">window.onload = function() { window.print(); }</script>')

        return response

    return HttpResponse('Erreur lors de la génération du PDF', status=500)


def print_devis(request, devis_id):
    # Obtenez l'objet Facture à partir de la base de données
    devis = get_object_or_404(Devis, pk=devis_id)

    # Chargez le modèle HTML de la facture
    template = get_template('devis_template.html')

    # Remplissez le modèle HTML avec les données de la facture
    context = {'devis': devis}
    html = template.render(context)

    # Créez un objet BytesIO pour stocker le PDF généré
    response = BytesIO()

    # Créez le PDF à partir du HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    # Vérifiez si la génération du PDF a réussi
    if not pdf.err:
        # Réponse avec le contenu PDF
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=devis_{devis.id}.pdf'

        # Ajoutez le script JavaScript pour déclencher l'impression automatiquement
        response.write('<script type="text/javascript">window.onload = function() { window.print(); }</script>')

        return response

    return HttpResponse('Erreur lors de la génération du PDF', status=500)






def delete_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    facture.delete()
    return redirect('factures_list')



def view_facture(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            return redirect('update_facture', facture_id=facture_id)
        elif 'delete' in request.POST:
            return redirect('delete_facture', facture_id=facture_id)
    else:
        form = FactureForm(instance=facture)
          
    return render(request, 'view_facture.html', {'facture': facture, 'form': form})




def view_devis(request, devis_id):
    devis = Devis.objects.get(pk=devis_id)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            return redirect('update_devis', devis_id=devis_id)
        elif 'delete' in request.POST:
            return redirect('delete_devis', devis_id=devis_id)
    else:
        form = DevisForm(instance=devis)
          
    return render(request, 'view_devis.html', {'devis': devis, 'form': form})





def delete_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        facture.delete()
        return redirect('factures_list')  # Rediriger vers la liste des factures après la suppression
    return render(request, 'delete_facture.html', {'facture': facture})




from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request, facture_id):
    # Obtenir la facture correspondante depuis votre modèle Django.
    facture = get_object_or_404(Facture, id=facture_id)

    # Charger le modèle HTML
    template = get_template('facture_template.html')
    context = {'facture': facture}

    # Remplir le modèle HTML avec les données de la facture
    html = template.render(context)

    # Créer un objet BytesIO pour stocker le PDF généré
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.numero_facture}.pdf"'

    # Convertir le modèle HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Une erreur s\'est produite lors de la création du PDF.', content_type='text/plain')
        
    return response





def generate_pdf1(request, devis_id):
    # Obtenir la facture correspondante depuis votre modèle Django.
    devis = get_object_or_404(Devis, id=devis_id)

    # Charger le modèle HTML
    template = get_template('devis_template.html')
    context = {'devis': devis}

    # Remplir le modèle HTML avec les données de la facture
    html = template.render(context)

    # Créer un objet BytesIO pour stocker le PDF généré
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="devis_{devis.numero_devis}.pdf"'

    # Convertir le modèle HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Une erreur s\'est produite lors de la création du PDF.', content_type='text/plain')
        
    return response



def dashboard(request):
    # Calculer les statistiques
    total_ventes = Facture.objects.aggregate(models.Sum('Total'))['Total__sum'] or 0
    total_clients = Client.objects.count()
    total_factures = Facture.objects.count()
    total_montant_paye = Facture.objects.filter(statut='paye').aggregate(models.Sum('Total'))['__sum'] or 0
    
    # Votre logique pour les autres statistiques

    # Enregistrer les statistiques dans la base de données ou les mettre à jour s'ils existent déjà
    statistique, created = Statistique.objects.get_or_create(pk=1)
    statistique.total_ventes = total_ventes
    statistique.total_clients = total_clients
    statistique.total_factures = total_factures
    statistique.total_montant_paye = total_montant_paye
    # Enregistrer la statistique mise à jour
    statistique.save()

    context = {
        'total_ventes': total_ventes,
        'total_clients': total_clients,
        'total_factures': total_factures,
        'total_montant_paye': total_montant_paye,
        # Ajoutez d'autres variables de contexte pour les autres statistiques
    }

    factures = Facture.objects.all()
    return render(request, 'dashboard.html', {'factures': factures})





def dashboard(request):
    # Calculer les statistiques
    total_ventes = Facture.objects.aggregate(Sum('Total'))['Total__sum'] or 0
    total_clients = Client.objects.count()
    total_factures = Facture.objects.count()
    total_devis = Devis.objects.count()
    # Votre logique pour les autres statistiques

    # Enregistrer les statistiques dans la base de données ou les mettre à jour s'ils existent déjà
    statistique, created = Statistique.objects.get_or_create(pk=1)
    statistique.total_ventes = total_ventes
    statistique.total_clients = total_clients
    statistique.total_factures = total_factures
    statistique.total_devis = total_devis
    # Enregistrer la statistique mise à jour
    statistique.save()

    context = {
        'total_ventes': total_ventes,
        'total_clients': total_clients,
        'total_factures': total_factures,
        'total_devis': total_devis,
            # Ajoutez d'autres variables de contexte pour les autres statistiques
    }

    factures = Facture.objects.all()
    return render(request, 'dashboard.html', {'factures': factures, **context})




