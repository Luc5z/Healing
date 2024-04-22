from django.contrib import admin
from .models import DatasAbertas, Especialidades, DadosMedico

admin.site.register(Especialidades)
admin.site.register(DadosMedico)
admin.site.register(DatasAbertas)