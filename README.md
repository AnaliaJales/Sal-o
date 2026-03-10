# 💇‍♀️ Salão Rainbow Hair - Sistema de Gerenciamento

Sistema de gerenciamento para salão de beleza desenvolvido em Django, permitindo o controle de clientes, serviços, profissionais e agendamentos.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-4.5-purple)
![License](https://img.shields.io/badge/License-MIT-blue)

## 📋 Índice

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Executando o Projeto](#executando-o-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Customização](#customização)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 📖 Descrição

O **Salão Rainbow Hair** é um sistema completo para gestão de salões de beleza, oferecendo interface intuitiva para agendamentos, cadastro de clientes, serviços e profissionais.

---

## ✨ Funcionalidades

- **📅 Agendamentos**: Gerenciamento completo de horários e compromissos
- **👥 Clientes**: Cadastro e histórico de clientes
- **✂️ Serviços**: Catálogo de serviços com preços e duração
- **👨‍💼 Profissionais**: Controle de colaboradores e especialidades
- **📊 Relatórios**: Dashboard com estatísticas do salão
- **👤 Gerenciamento de Usuários**: Sistema de autenticação e permissões

---

## 🛠️ Tecnologias

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 4, HTML5, CSS3
- **Database**: dbSqlite
- **Bibliotecas**:
  - django-soft-delete
  - python-decouple
  - mysqlclient

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8+
- Git (opcional)

---

## 🚀 Instalação

Siga os passos abaixo para configurar o projeto em sua máquina:

### Passo 1: Criar o Ambiente Virtual

```bash
# No Windows PowerShell
py -m venv venv
```

### Passo 2: Ativar o Ambiente Virtual

```bash
# No Windows PowerShell
.\venv\Scripts\activate.ps1
```

### Passo 3: Instalar as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Instalar o Django e Pacotes Adicionais

```bash
python -m pip install django
pip install django-soft-delete
pip install python-decouple
python -m pip install mysqlclient
```

### Passo 5: Criar as Migrações do Banco de Dados

```bash
python manage.py makemigrations
```

### Passo 6: Aplicar as Migrações

```bash
python manage.py migrate
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do Banco de Dados
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306

# Configurações do Django
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Criar Superusuário (Opcional)

Para acessar o painel admin do Django:

```bash
python manage.py createsuperuser
```

---

## ▶️ Executando o Projeto

Após completar a instalação, inicie o servidor:

```bash
python manage.py runserver
```

Acesse o sistema em: **http://127.0.0.1:8000/**

---

## 📂 Estrutura do Projeto

```
Salão_Rainbow_HairCT/
├── Salão/                      # Diretório principal do projeto Django
│   ├── __init__.py
│   ├── settings.py            # Configurações do projeto
│   ├── urls.py                # URLs principais
│   ├── wsgi.py
│   └── ...
├── agendamentos/              # Aplicativo principal
│   ├── migrations/
│   ├── templates/             # Templates HTML
│   ├── models.py              # Modelos do banco de dados
│   ├── views.py               # Views do sistema
│   ├── urls.py                # URLs do app
│   └── admin.py
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
├── media/                     # Arquivos de mídia uploadados
├── requirements.txt           # Dependências do Python
├── manage.py                  # Script de gerenciamento Django
├── GUIA_CUSTOMIZACAO.md       # Guia de customização de cores
└── MUDANCAS_DESIGN.md         # Documentação das mudanças de design
```

---

## 🎨 Customização

### Cores do Tema

O sistema utiliza um tema personalizado com as seguintes cores:

| Cor | Hex | Uso |
|-----|-----|-----|
| Primária | #b08671 | Navbar, botões principais |
| Secundária | #d2b48c | Destaques, botões de sucesso |
| Fundo | #f8f9fa | Fundo das seções |

### Alterando Cores

Para customizar as cores, edite o arquivo `agendamentos/templates/base.html` conforme as instruções em `GUIA_CUSTOMIZACAO.md`.

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 📞 Suporte

Em caso de dúvidas ou problemas, consulte:

- [Documentação do Django](https://docs.djangoproject.com/)
- [Documentação do Bootstrap](https://getbootstrap.com/docs/4.5/)
- Arquivo `GUIA_CUSTOMIZACAO.md` para customização de design
- Arquivo `MUDANCAS_DESIGN.md` para informações sobre o template

---

**Desenvolvido com ❤️ para o Salão Rainbow Hair**

