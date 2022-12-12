from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static

from . import views
  
urlpatterns = [
    path('cadastro',views.cadastro, name='cadastro'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('cria/receita', views.cria_receita, name='cria_receita'),
    path('deleta/<int:receita_id>',views.deleta_receita, name='deletando_receita'),
    path('edita/<int:receita_id>',views.edita_receita, name='editando_receita'),
    path('atualiza_receita', views.atualiza_receita, name='atualizando_receita'),
]