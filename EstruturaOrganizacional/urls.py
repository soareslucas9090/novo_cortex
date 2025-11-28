from django.urls import path, include

app_name = 'estrutura-organizacional'

urlpatterns = [
    path('campus/', include('EstruturaOrganizacional.campus.urls')),
]
