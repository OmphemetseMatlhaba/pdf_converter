from django.contrib import admin
from . import views
from .models import UploadedPDF

# Register your models here.

admin.site.register(UploadedPDF)