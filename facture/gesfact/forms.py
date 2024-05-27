from django import forms
from .models import Client, Article, Devis, Facture, Profile

class ClientForm(forms.ModelForm):
    total_factures = forms.DecimalField(disabled=True, required=False)
    class Meta:
        model = Client
        fields = ['identifiant', 'nom', 'telephone', 'email', 'total_factures','datecreation', 'adressefacturation']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'description', 'cout_unitaire','reference']

class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['numero_devis', 'client', 'article', 'datecreation', 'quantite', 'serie', 'Tot', 'remise']

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture                                                                                  
        fields = ['numero_facture', 'client','datecreation', 'date_emission', 'article', 'quantite', 'serie', 'remise', 'montant_paye', 'Total', 'statut', 'frais_liv', 'rest', 'adresseemission']




class AddProfileForm(forms.Form):
    employee_name = forms.CharField(max_length=100, required=True, label="Nom complet")
    email = forms.EmailField(required=True, label="Email")
    numero_telephone = forms.CharField(max_length=15, required=True, label="Téléphone")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirmer le mot de passe")


class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


class LogForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
