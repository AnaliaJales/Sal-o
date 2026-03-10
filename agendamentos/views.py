from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

from .models import Agendamento, Cliente, Servico, Profissional
from .forms import AgendamentoForm, ClienteForm, ServicoForm, ProfissionalForm


def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        from django.shortcuts import render
        return render(self.request, '403.html', status=403)


class RecepcionistaRequiredMixin(UserPassesTestMixin):
    """Mixin that allows only users in 'Recepcionista' group or admin users"""
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        # Allow admin users (staff or superuser)
        if user.is_staff or user.is_superuser:
            return True
        # Check if user is in Recepcionista group
        return user.groups.filter(name='Recepcionista').exists()
    
    def handle_no_permission(self):
        from django.shortcuts import render
        return render(self.request, '403.html', status=403)


class HomeView(TemplateView):
    template_name = 'home.html'

class IndexView(LoginRequiredMixin, ListView):
    model = Agendamento
    template_name = 'index.html'
    context_object_name = 'agendamentos'
    ordering = ['-data_hora']

    def get_queryset(self):
        Agendamento.atualizar_statuss()
        return Agendamento.objects.select_related(
            'cliente', 'servico', 'profissional'
        ).order_by('-data_hora')


class AddAgendamentoView(LoginRequiredMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'add_agendamentos.html'
    success_url = reverse_lazy('agendamentos:index')


class EditAgendamentoView(LoginRequiredMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'edit_agendamentos.html'
    success_url = reverse_lazy('agendamentos:index')


class AgendamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos:index')


class RelatoriosView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "relatorios.html"


class DadosRelatorioView(LoginRequiredMixin, AdminRequiredMixin, View):

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        total = agendamentos.count()

        por_dia = (
            agendamentos
            .annotate(dia=TruncDay('data_hora'))
            .values('dia')
            .annotate(total=Count('id'))
            .order_by('dia')
        )

        total_clientes = Cliente.objects.distinct().count()
        total_faturamento = agendamentos.aggregate(
            total=Sum('servico__preco')
        )['total'] or 0

        return JsonResponse({
            'total': total,
            'total_clientes': total_clientes,
            'total_agendamentos_abertos': Agendamento.objects.filter(status='AGENDADO').count(),
            'total_faturamento': float(total_faturamento),
            'por_dia': {
                str(item['dia'].date()): item['total']
                for item in por_dia
            }
        })


class DadosRelatorioFaturamentoView(LoginRequiredMixin, AdminRequiredMixin, View):

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))
        periodo = request.GET.get('periodo', 'dia')

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        total_faturamento = agendamentos.aggregate(
            total=Sum('servico__preco')
        )['total'] or 0

        trunc = TruncMonth if periodo == 'mes' else TruncDay

        por_periodo = (
            agendamentos
            .annotate(periodo=trunc('data_hora'))
            .values('periodo')
            .annotate(
                total=Sum('servico__preco'),
                quantidade=Count('id')
            )
                .order_by('periodo')
            )
        dados = {
                str(item['periodo'].date()): {
                'total': float(item['total'] or 0),
                'quantidade': item['quantidade']
            }
            for item in por_periodo
        }

        return JsonResponse({
            'total_faturamento': float(total_faturamento),
            'por_periodo': dados
        })


class UsuariosView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "usuarios.html"
    context_object_name = "usuarios"


class EditUsuarioView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'is_staff']
    template_name = "edit_usuarios.html"
    success_url = reverse_lazy('agendamentos:usuarios')


class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # Adicionar o usuário ao grupo "Recepcionista"
        recepcionista_group = Group.objects.get_or_create(name='Recepcionista')[0]
        user.groups.add(recepcionista_group)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_obj'] = self.request.user
        return ctx


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente_list.html"
    context_object_name = "clientes"


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente_form.html"
    success_url = reverse_lazy('agendamentos:cliente-list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente_form.html"
    success_url = reverse_lazy('agendamentos:cliente-list')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "cliente_confirm_delete.html"
    success_url = reverse_lazy('agendamentos:cliente-list')


class ServicoListView(LoginRequiredMixin, ListView):
    model = Servico
    template_name = "servico_list.html"
    context_object_name = "servicos"


class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy('agendamentos:servico-list')


class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy('agendamentos:servico-list')


class ServicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Servico
    template_name = "servico_confirm_delete.html"
    success_url = reverse_lazy('agendamentos:servico-list')


class ProfissionalListView(LoginRequiredMixin, RecepcionistaRequiredMixin, ListView):
    model = Profissional
    template_name = "profissional_list.html"
    context_object_name = "profissionais"


class ProfissionalCreateView(LoginRequiredMixin, RecepcionistaRequiredMixin, CreateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = "profissional_form.html"
    success_url = reverse_lazy('agendamentos:profissional-list')


class ProfissionalUpdateView(LoginRequiredMixin, RecepcionistaRequiredMixin, UpdateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = "profissional_form.html"
    success_url = reverse_lazy('agendamentos:profissional-list')


class ProfissionalDeleteView(LoginRequiredMixin, RecepcionistaRequiredMixin, DeleteView):
    model = Profissional
    template_name = "profissional_confirm_delete.html"
    success_url = reverse_lazy('agendamentos:profissional-list')


class DadosRelatorioServicosView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Most popular services report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_servico = (
            agendamentos
            .values('servico__nome', 'servico__preco')
            .annotate(
                quantidade=Count('id'),
                total_faturado=Sum('servico__preco')
            )
            .order_by('-quantidade')
        )

        return JsonResponse({
            'servicos': [
                {
                    'nome': item['servico__nome'],
                    'preco': float(item['servico__preco']),
                    'quantidade': item['quantidade'],
                    'total_faturado': float(item['total_faturado'] or 0)
                }
                for item in por_servico
            ]
        })


class DadosRelatorioProfissionaisView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Professionals performance report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('profissional', 'servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_profissional = (
            agendamentos
            .values('profissional__nome', 'profissional__especialidade')
            .annotate(
                quantidade=Count('id'),
                total_faturado=Sum('servico__preco')
            )
            .order_by('-quantidade')
        )

        return JsonResponse({
            'profissionais': [
                {
                    'nome': item['profissional__nome'],
                    'especialidade': item['profissional__especialidade'],
                    'quantidade': item['quantidade'],
                    'total_faturado': float(item['total_faturado'] or 0)
                }
                for item in por_profissional
            ]
        })


class DadosRelatorioStatusView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Appointments by status report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.all()

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_status = (
            agendamentos
            .values('status')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        return JsonResponse({
            'status': [
                {
                    'status': item['status'],
                    'total': item['total']
                }
                for item in por_status
            ],
            'total_geral': agendamentos.count()
        })


class DadosRelatorioClientesView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Top clients report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('cliente', 'servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_cliente = (
            agendamentos
            .values('cliente__nome', 'cliente__telefone')
            .annotate(
                quantidade=Count('id'),
                total_gasto=Sum('servico__preco')
            )
            .order_by('-total_gasto')[:10]  # Top 10 clients
        )

        return JsonResponse({
            'clientes': [
                {
                    'nome': item['cliente__nome'],
                    'telefone': item['cliente__telefone'],
                    'quantidade': item['quantidade'],
                    'total_gasto': float(item['total_gasto'] or 0)
                }
                for item in por_cliente
            ]
        })
