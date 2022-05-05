from django.contrib import admin
from .models import User, Cliente, Planta, Role, Contacto

# Register your models here.
admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Planta)
admin.site.register(Role)
admin.site.register(Contacto)