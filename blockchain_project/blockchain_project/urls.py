"""blockchain_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blockchain_app import views

app_name = 'blockchain_app'

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mine', views.mine, name='mine'),
    path('chain', views.full_chain, name='full_chain'),
    path('/transactions/new', views.new_transaction, name='new_transaction'),
    path('/nodes/register', views.register_nodes, name='register_nodes'),
    path('/nodes/resolve', views.resolve_nodes, name='resolve_nodes'),
]
