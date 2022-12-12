from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        Nome = request.POST['nome']
        Email = request.POST['email']
        Senha = request.POST['password']
        Senha2 = request.POST['password2']

        if campo_vazio(Nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(Email):
            messages.error(request, 'O campo email não pode ficar em branco')
            return redirect('cadastro')
        if senhas_nao_sao_iguais(Senha, Senha2):
            messages.error(request, 'As senhas não coincidem')
            return redirect('cadastro')
        
        if User.objects.filter(email=Email).exists():
            messages.error(request, 'Email ou usuário já existentes ou indisponíveis')
            return redirect('cadastro')

        if User.objects.filter(email=Email).exists():
            messages.error(request, 'Email ou usuário já existentes ou indisponíveis')
            return redirect('cadastro')

        if User.objects.filter(username=Nome).exists():
            messages.error(request, 'Email ou usuário já existentes ou indisponíveis')
            return redirect('cadastro')

        user = User.objects.create_user(username=Nome, email=Email, password=Senha)
        user.save()
        messages.success(request, 'Olá '+Nome+', seu cadastro foi realizado com sucesso')
        print(Nome, Email, Senha, Senha2)
        return redirect('login')
    else:
            return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        Email = request.POST['email']
        Senha = request.POST['password']
        if Email == "" or Senha == "":
            print("Informe email ou senha")
            return redirect('login')
        print(Email, Senha)
        if User.objects.filter(email=Email).exists():
            Nome = User.objects.filter(email=Email).values_list('username', flat=True).get()
            print(Nome)
            user = auth.authenticate(request, username=Nome, password=Senha)
            if user is not None:
                auth.login(request, user)
                print('login realizado com sucesso')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def cria_receita(request):


    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        print(nome_receita, ingredientes)
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')

def campo_vazio(campo):
    return not campo.strip()

def senhas_nao_sao_iguais(senha1, senha2):
    return senha1 != senha2

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    messages.success(request, 'Receita deletada com sucesso')
    return redirect('dashboard')

def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = { 'receita':receita }
    return render(request, 'usuarios/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')