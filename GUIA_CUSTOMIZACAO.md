# 🎨 Guia de Customização - Design Careo

## Como Personalizar as Cores

### 1. Alterar Cor Primária (Tema Bege/Marrom)

No arquivo `base.html`, procure pelas cores utilizadas nos gradientes primários e substitua conforme desejado. As cores atuais são:

```css
/* Gradiente bege/marrom atual */
background: linear-gradient(135deg, #b08671 0%, #6b4f4f 100%);

/* Exemplo: Para azul */
background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);

/* Exemplo: Para verde */
background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
```

### 2. Alterar Cor Secundária (Tom Claro)

Procure pelos gradientes usados em botões de sucesso e ícones, atualmente:

```css
/* Tom claro atual */
background: linear-gradient(135deg, #d2b48c 0%, #a1866f 100%);

/* Exemplo: Para laranja */
background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
```

### 3. Alterar Cor de Fundo

Procure por `#f8f9fa`:

```css
/* Cinza atual */
background-color: #f8f9fa;

/* Exemplo: Para branco puro */
background-color: #ffffff;
```

## Como Adicionar Logo

1. Crie uma pasta `static/images/` na raiz do projeto
2. Coloque sua logo em `static/images/logo.png`
3. No `base.html`, localize a navbar-brand e adicione:

```html
<a class="navbar-brand" href="{% url 'home' %}">
    <img src="{% static 'images/logo.png' %}" alt="Logo" height="40">
    Salão Rainbow Hair
</a>
```

4. Adicione no topo do `base.html`:
```html
{% load static %}
```

## Como Customizar Fontes

### Alterar Poppins para Outra Fonte

No `<head>` do `base.html`:

```html
<!-- De -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Para Roboto -->
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
```

Depois altere no CSS:
```css
body {
    font-family: 'Roboto', sans-serif;
}
```

## Como Adicionar Imagens de Fundo

### Na Home (Hero Section)

Edite o `home.html` e localize `.hero-section`:

```css
.hero-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)), 
                url('{% static "images/hero.jpg" %}') center/cover;
    color: white;
    padding: 80px 0;
}
```

## Como Alterar Ícones

Todos os ícones usam **Font Awesome 6**. Veja mais em: https://fontawesome.com/icons

Exemplos:
```html
<!-- Spa -->
<i class="fas fa-spa"></i>

<!-- Tesoura -->
<i class="fas fa-cut"></i>

<!-- Paleta -->
<i class="fas fa-palette"></i>

<!-- Coração -->
<i class="fas fa-heart"></i>

<!-- Usuário -->
<i class="fas fa-user"></i>

<!-- Configurações -->
<i class="fas fa-cog"></i>
```

## Como Criar Novos Templates

Sempre estenda de `base.html`:

```django
{% extends 'base.html' %}

{% block title %}Seu Título{% endblock %}

{% block extra_css %}
<style>
    /* Seus estilos customizados */
</style>
{% endblock %}

{% block content %}
    <!-- Seu conteúdo aqui -->
{% endblock %}

{% block extra_js %}
<script>
    // Seus scripts aqui
</script>
{% endblock %}
```

## Dicas de Design

### 1. Consistência de Cores
- Use a cor primária para ações principais
- Use a cor secundária para destaques
- Mantenha o cinza para fundo

### 2. Espaçamento
- Use múltiplos de 5px ou 10px
- `margin` e `padding` devem ser consistentes
- Use classes Bootstrap (`mb-3`, `mt-4`, etc)

### 3. Sombras
- Leve: `box-shadow: 0 2px 5px rgba(0,0,0,0.1);`
- Média: `box-shadow: 0 5px 15px rgba(0,0,0,0.1);`
- Forte: `box-shadow: 0 10px 25px rgba(0,0,0,0.15);`

### 4. Animations
```css
transition: all 0.3s ease;
```

## Variáveis de Cores (para referência)

| Cor | Hex | Uso |
|-----|-----|-----|
| Primária 1 | #b08671 | Navbar, botões |
| Primária 2 | #6b4f4f | Gradiente |
| Secundária 1 | #d2b48c | Botões de sucesso |
| Secundária 2 | #a1866f | Gradiente de sucesso |
| Fundo | #f8f9fa | Seções de fundo |
| Cinza | #666 | Texto secundário |
| Escuro | #333 | Títulos |
| Erro | #dc3545 | Alertas de erro |
| Sucesso | #28a745 | Confirmações |
| Aviso | #ffc107 | Avisos |

## Modificar Layout da Navbar

No `base.html`, localize a seção `<!-- Navigation Bar -->` e customize:

```html
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    <div class="container">
        <!-- Seu conteúdo -->
    </div>
</nav>
```

### Remover Sticky (fixo)
```html
<nav class="navbar navbar-expand-lg navbar-dark">
```

### Alterar Posição
```html
<nav class="navbar navbar-expand-lg navbar-dark navbar-fixed-top">
```

## Media Queries (Responsividade)

Para adicionar estilos só em mobile:

```css
@media (max-width: 768px) {
    .seu-elemento {
        /* Estilos para mobile */
    }
}
```

## Troubleshooting

### Os estilos não aplicam?
1. Limpe o cache do navegador (Ctrl+F5)
2. Verifique se a CDN do Bootstrap está carregando
3. Use Chrome DevTools (F12) para debugar

### Ícones não aparecem?
1. Verifique se Font Awesome está carregando
2. Use `<i class="fas fa-..."></i>` com o prefixo `fas`
3. Consulte https://fontawesome.com/icons

### Layout quebrado em mobile?
1. Verifique as classes Bootstrap responsivas
2. Use `col-md-6` para tablets, `col-12` para mobile
3. Teste com `python manage.py runserver` e acesse via dispositivo móvel

---

**Dúvidas?** Consulte a documentação do Bootstrap 4: https://getbootstrap.com/docs/4.5/
