from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models



class Client(models.Model):
    identifiant = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    email = models.EmailField()
    datecreation = models.DateField(default=timezone.now)
    adressefacturation = models.CharField(max_length=300, default='Votre adresse')
    
    def total_factures(self):
        return self.facture_set.count()

    def __str__(self):
        return self.nom




class Article(models.Model):
    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, default='la réference')
    description = models.TextField(null=True)
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom




class Devis(models.Model):
    datecreation = models.DateField(default=timezone.now, blank=True)
    numero_devis = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_emission = models.DateField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    serie = models.CharField(max_length=50)
    Tot = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pdf_file = models.FileField(upload_to='devis/pdfs/', null=True, blank=True)

    def __str__(self):
        return self.numero_devis
    
    def montant_total_apres_remise(self):
        montant_total = self.article.cout_unitaire * self.quantite
        remise_amount = montant_total * (self.remise / 100)
        montant_final = montant_total - remise_amount
        return montant_final

    def save(self, *args, **kwargs):
        self.Tot = self.montant_total_apres_remise()
        super().save(*args, **kwargs)






class Facture(models.Model):
    STATUT_CHOICES = (
        ('paye', 'Payé'),
        ('partiellement_paye', 'Partiellement payé'),
        ('impaye', 'Impayé'),
    )
    numero_facture = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_emission = models.DateField(default=timezone.now)
    datecreation = models.DateField(default=timezone.now, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    serie = models.CharField(max_length=100)
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='impaye')
    Total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    frais_liv = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adresseemission = models.CharField(max_length=300, default='Votre adresse')

    def restant(self):
        res = self.Total - self.montant_paye
        return res

    def total(self):
        montant_total = self.article.cout_unitaire * self.quantite
        remise_amount = montant_total * (self.remise / 100)
        montant_final = montant_total - remise_amount + self.frais_liv
        return montant_final

    def save(self, *args, **kwargs):
        self.Total = self.total()
        self.rest = self.Total - self.montant_paye
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_facture





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    numero_telephone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username





class Statistique(models.Model):
    total_ventes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_clients = models.PositiveIntegerField(default=0)
    total_factures = models.PositiveIntegerField(default=0)
    total_montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "Statistiques"

    class Meta:
        verbose_name_plural = "Statistiques"
