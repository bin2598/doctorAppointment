from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('book', views.book_appointment, name='book'),
    path('patient', views.patient, name='patient'),
    path('doctor', views.doctor, name='doctor'),
    path('doctor_appointment/<i>', views.doctor_appointment),
    path('logout', views.logout),
]