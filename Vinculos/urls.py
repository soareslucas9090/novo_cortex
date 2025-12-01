from django.urls import path, include

app_name = 'vinculos'

urlpatterns = [
    path('campus/', include('EstruturaOrganizacional.campus.urls')),
]
