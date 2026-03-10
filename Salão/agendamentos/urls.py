from django.urls import path
from .views import *


app_name = 'agendamentos'


urlpatterns = [

    #iniciais
    path('', HomeView.as_view(), name='home'), 
    path('dashboard/', IndexView.as_view(), name='index'), 
 
    #relatorio
    path('relatorios/', RelatoriosView.as_view(), name='relatorios'), 
    path('relatorios/dados/', DadosRelatorioView.as_view(), name='dados-relatorio'),
    path('relatorios/faturamento/', DadosRelatorioFaturamentoView.as_view(), name='dados-relatorio-faturamento'),
    path('relatorios/servicos/', DadosRelatorioServicosView.as_view(), name='dados-relatorio-servicos'),
    path('relatorios/profissionais/', DadosRelatorioProfissionaisView.as_view(), name='dados-relatorio-profissionais'),
    path('relatorios/status/', DadosRelatorioStatusView.as_view(), name='dados-relatorio-status'),
    path('relatorios/clientes/', DadosRelatorioClientesView.as_view(), name='dados-relatorio-clientes'),
    #usuarios
    path('usuarios/', UsuariosView.as_view(), name='usuarios'), 
    path('usuarios/edit/<int:pk>/', EditUsuarioView.as_view(), name='edit-usuario'), 
    path('perfil/', ProfileView.as_view(), name='perfil'),
    path('register/', RegisterView.as_view(), name='register'), 

    #agendamentos
    path('agendamento/add/', AddAgendamentoView.as_view(), name='add-agendamento'), 
    path('agendamento/edit/<int:pk>/', EditAgendamentoView.as_view(), name='edit-agendamento'), 
    path('agendamento/delete/<int:pk>/', AgendamentoDeleteView.as_view(), name='delete-agendamento'),
    #cliente
    path('clientes/', ClienteListView.as_view(), name='cliente-list'), 
    path('clientes/add/', ClienteCreateView.as_view(), name='cliente-create'), 
    path('clientes/edit/<int:pk>/', ClienteUpdateView.as_view(), name='cliente-update'), 
    path('clientes/delete/<int:pk>/', ClienteDeleteView.as_view(), name='cliente-delete'), 
    #serviço
    path('servicos/', ServicoListView.as_view(), name='servico-list'), 
    path('servicos/add/', ServicoCreateView.as_view(), name='servico-create'), 
    path('servicos/edit/<int:pk>/', ServicoUpdateView.as_view(), name='servico-update'), 
    path('servicos/delete/<int:pk>/', ServicoDeleteView.as_view(), name='servico-delete'), 
    #profissional
    path('profissionais/', ProfissionalListView.as_view(), name='profissional-list'), 
    path('profissionais/edit/<int:pk>/', ProfissionalUpdateView.as_view(), name='profissional-update'), 
    path('profissionais/delete/<int:pk>/', ProfissionalDeleteView.as_view(), name='profissional-delete'), 
    path('profissionais/add/', ProfissionalCreateView.as_view(), name='profissional-create') 
]