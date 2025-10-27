# Templates da Aplicação Principal

Este diretório contém os templates base do projeto ProjSala, demonstrando conceitos de **herança** e **inclusão** de templates no Django, utilizando o framework CSS **Bulma**.

## Estrutura dos Templates

### 1. Templates de Inclusão (Include)

Estes templates são incluídos no `base.html` usando a tag `{% include %}`:

#### `header.html`
- **Descrição**: Cabeçalho do projeto com hero section e navbar
- **Componentes**:
  - Hero section com título e subtítulo
  - Barra de navegação responsiva com links para as aplicações
  - Menu burger para dispositivos móveis
  - Ícones Font Awesome

#### `sidebar.html`
- **Descrição**: Barra de navegação lateral com menu de aplicações
- **Componentes**:
  - Menu principal com links para página inicial
  - Menu de aplicações (Enquete, IMC) com submenus
  - Menu de informações (Documentação, Ajuda, Contato)
  - Card com dica de uso
  - Links ativos destacados

#### `footer.html`
- **Descrição**: Rodapé do projeto com informações e links
- **Componentes**:
  - Informações sobre o projeto
  - Links úteis para documentação
  - Informações de copyright
  - Layout responsivo em colunas

### 2. Template Base (Herança)

#### `base.html`
- **Descrição**: Template base que todas as outras páginas herdam
- **Funcionalidades**:
  - Estrutura HTML5 completa
  - Inclusão do Bulma CSS via CDN
  - Inclusão do Font Awesome para ícones
  - Layout flexível com header, sidebar, conteúdo e footer
  - Sistema de blocos Django para customização

**Blocos disponíveis**:
- `title`: Título da página (tag `<title>`)
- `extra_css`: CSS adicional
- `breadcrumb`: Navegação breadcrumb
- `breadcrumb_items`: Itens do breadcrumb
- `page_header`: Cabeçalho da página
- `page_title`: Título principal
- `page_subtitle`: Subtítulo
- `content`: Conteúdo principal (OBRIGATÓRIO)
- `extra_content`: Conteúdo adicional
- `extra_js`: JavaScript adicional

### 3. Template de Exemplo

#### `index.html`
- **Descrição**: Página inicial que demonstra herança do `base.html`
- **Demonstra**:
  - Uso de `{% extends 'principal/base.html' %}`
  - Sobrescrita de múltiplos blocos
  - Cards com informações das aplicações
  - Layout responsivo em colunas
  - Animações CSS

## Como Usar

### Criando uma Nova Página

Para criar uma nova página que use o template base:

```django
{% extends 'principal/base.html' %}

{% block title %}Minha Página - ProjSala{% endblock %}

{% block breadcrumb_items %}
<li class="is-active"><a href="#" aria-current="page">Minha Página</a></li>
{% endblock %}

{% block page_title %}
Título da Minha Página
{% endblock %}

{% block content %}
<!-- Seu conteúdo aqui -->
<div class="box">
    <h2 class="title">Olá, Mundo!</h2>
    <p>Este é meu conteúdo personalizado.</p>
</div>
{% endblock %}
```

### Incluindo Templates

Para incluir um template parcial em qualquer lugar:

```django
{% include 'principal/header.html' %}
```

## Recursos Utilizados

### Frameworks e Bibliotecas

- **Bulma CSS v0.9.4**: Framework CSS moderno e responsivo
  - Documentação: https://bulma.io/documentation/
  
- **Font Awesome v6.4.0**: Biblioteca de ícones
  - Documentação: https://fontawesome.com/

### Componentes Bulma Utilizados

- **Hero**: Seção de destaque no header
- **Navbar**: Barra de navegação responsiva
- **Menu**: Menu lateral com submenus
- **Box**: Containers com bordas e sombra
- **Card**: Cards de conteúdo
- **Columns**: Sistema de grid responsivo
- **Notification**: Mensagens de notificação
- **Message**: Caixas de mensagem estilizadas
- **Breadcrumb**: Navegação hierárquica
- **Footer**: Rodapé estilizado

## Estrutura Visual

```
┌─────────────────────────────────────────┐
│            HEADER (hero + navbar)       │
├──────────┬──────────────────────────────┤
│          │                              │
│ SIDEBAR  │        CONTEÚDO              │
│          │                              │
│  Menu    │   - Breadcrumb               │
│  Lateral │   - Título                   │
│          │   - Conteúdo Principal       │
│          │                              │
├──────────┴──────────────────────────────┤
│            FOOTER                       │
└─────────────────────────────────────────┘
```

## Responsividade

- **Desktop (>= 1024px)**: Layout com sidebar à esquerda e conteúdo à direita
- **Tablet (768px - 1023px)**: Layout adaptado com sidebar reduzida
- **Mobile (< 768px)**: Sidebar movida para baixo, navbar com menu burger

## Personalização

### Cores Bulma Usadas

- `is-primary`: Azul principal
- `is-info`: Azul claro informativo
- `is-success`: Verde de sucesso
- `is-warning`: Amarelo de alerta
- `is-danger`: Vermelho de erro
- `is-light`: Tons claros
- `is-dark`: Tons escuros

### CSS Customizado

O `base.html` inclui CSS customizado para:
- Layout flexível (flexbox) para footer fixo no rodapé
- Transições suaves em links
- Altura mínima do conteúdo
- Responsividade da sidebar

## Boas Práticas Implementadas

1. ✅ Separação de responsabilidades (header, sidebar, footer separados)
2. ✅ Reutilização de código através de includes
3. ✅ Herança de templates com blocos bem definidos
4. ✅ Design responsivo mobile-first
5. ✅ Acessibilidade com ARIA labels
6. ✅ Estrutura semântica do HTML5
7. ✅ Comentários explicativos no código
8. ✅ Uso de CDN para performance

## Exemplo de Aplicação

Para usar esses templates em outras aplicações do projeto (enquete, imc), basta fazer:

```django
{% extends 'principal/base.html' %}

{% block content %}
<!-- Conteúdo específico da aplicação -->
{% endblock %}
```

Isso garante que todas as aplicações tenham o mesmo layout e aparência, mantendo a consistência visual do projeto.
