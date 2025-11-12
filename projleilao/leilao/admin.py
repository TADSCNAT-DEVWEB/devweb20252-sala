from django.contrib import admin
from .models import Participante, Leilao, ItemLeilao, Lance
# Register your models here.

admin.site.register(Participante)
admin.site.register(Leilao)
admin.site.register(ItemLeilao)
admin.site.register(Lance)