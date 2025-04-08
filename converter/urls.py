from django.urls import path
from converter import views

urlpatterns = [
   
    path('', views.convert_pdf_view, name='convert_pdf_view'),
    path('advice/', views.get_advice, name='get_advice'),
]
