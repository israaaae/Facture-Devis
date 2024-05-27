from django.contrib import admin
from .models import Client
from .models import Article
from .models import Facture
from .models import Devis
from .models import Profile
admin.site.register(Client)
admin.site.register(Article)
admin.site.register(Facture)
admin.site.register(Devis)
admin.site.register(Profile)
