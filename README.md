# Cortex API - IFPI Campus Floriano

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)

Reformulação completa da **API Cortex**, plataforma institucional para servir dados de forma segura e estruturada para aplicações do **IFPI - Campus Floriano**.

Esta versão representa uma evolução do projeto anterior, com uma nova arquitetura em camadas que promove separação clara de responsabilidades, manutenibilidade e escalabilidade.

---

## 📖 Sobre o Projeto

O **Cortex API** é uma API REST centralizada para servir dados institucionais do IFPI Campus Floriano. 

- Segue o padrão **REST** (não 100% RESTful, equilibrando desempenho e simplicidade)
- **Autenticação via JWT** (SimpleJWT)
- **Documentação interativa** via Swagger (drf-spectacular)
- **Arquitetura em camadas** para organização do código

---

## 🔧 Stack Técnica

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Django** | 5.2.7 | Framework web |
| **Django Rest Framework** | 3.16.1 | REST Framework |
| **PostgreSQL** | 13+ | Banco de dados (SQLite para desenvolvimento) |
| **SimpleJWT** | 5.5.1 | Autenticação JWT (Access Token 30min, Refresh Token 7 dias) |
| **drf-spectacular** | 0.28.0 | Documentação Swagger/ReDoc |
| **django-simple-history** | 3.10.1 | Auditoria de mudanças |
| **django-cors-headers** | 4.9.0 | Configuração CORS |
| **Gunicorn** | - | Deploy Linux |
| **Waitress** | - | Deploy Windows |
| **WhiteNoise** | - | Static Files |
| **SMTP** | - | Email (padrão Gmail) |

---

## 🏗️ Arquitetura em Camadas

O projeto implementa uma arquitetura modular de 4 camadas bem definidas.

### ⚠️ Princípio Fundamental: Views Leves

**Views devem ser "burras"**: Apenas recebem dados, delegam para o Business, e retornam resposta.

### Hierarquia de Chamadas

```
View (entrada/saída)
  └── Business (orquestração)
        ├── Rules (validações)
        ├── Helpers (queries/utils)
        └── State (transições de estado)
```

### Camadas

| Camada | Arquivo | Responsabilidade |
|--------|---------|------------------|
| **Business** | `business.py` | Orquestra COMO fazer operações (CRUD, workflows complexos) |
| **Rules** | `rules.py` | Valida SE uma ação pode ser executada (retorna `bool` ou lança exceção) |
| **Helpers** | `helpers.py` | Fornece ferramentas (queries customizadas, formatações, utils) |
| **State** | `state.py` | Máquina de estados (futuro) |

**Importante:**
- Views só chamam **Business**
- Business pode chamar **Rules**, **Helpers** e **State**
- Rules, Helpers e State **NÃO** chamam uns aos outros diretamente

---

## ✨ Recursos Implementados

- ✅ Gerenciamento completo de usuários (Servidor, Aluno, Terceirizado, Estagiário)
- ✅ Estrutura organizacional (Campus, Setores, Empresas, Cargos, Atividades, Funções)
- ✅ Vínculos (Matrículas)
- ✅ Sistema de permissões
- ✅ Autenticação JWT
- ✅ Documentação Swagger completa e interativa
- ✅ Auditoria automática de mudanças (django-simple-history)

---

## 🚀 Instalação e Configuração

### Requisitos

- Python 3.10 ou superior (recomendado 3.11)
- PostgreSQL (ou SQLite para desenvolvimento)

### Setup

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (criar arquivo .env)
# Ver seção "Variáveis de Ambiente" abaixo

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos (necessário para Swagger)
python manage.py collectstatic

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor de desenvolvimento
python manage.py runserver
```

---

## 🔐 Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Django Settings
DJANGO_SECRET_KEY=sua_chave_secreta_do_django
DJANGO_DEBUG=True  # Usar False em produção
ALLOWED_HOSTS=localhost,127.0.0.1  # Em produção, especificar domínios reais

# CORS e CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ORIGIN_WHITELIST=http://localhost:3000,http://127.0.0.1:3000
INTERNAL_IPS=127.0.0.1,localhost

# Database (PostgreSQL)
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=nome_do_banco
DATABASE_USER=usuario_do_banco
DATABASE_PASSWORD=senha_do_banco
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email (configuração padrão para Gmail)
DEFAULT_FROM_EMAIL=seu_email@gmail.com
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Nota:** Para desenvolvimento, pode-se omitir as variáveis de banco de dados (usará SQLite por padrão).

---

## 🖥️ Executando em Produção

### Linux (Gunicorn)

```bash
gunicorn BaseDRFApp.wsgi --workers 2 --bind :8000 --access-logfile -
```

### Windows (Waitress)

```bash
waitress-serve --port=8000 BaseDRFApp.wsgi:application
```

---

## 📚 Documentação da API

Acesse a documentação interativa Swagger em:

| Endpoint | Descrição |
|----------|-----------|
| `/api/schema/swagger/` | Swagger UI |
| `/api/schema/redoc/` | ReDoc |
| `/api/schema/` | Schema JSON |

### Autenticação na documentação

1. Acesse `/api/token/` para obter o token de acesso
2. Clique em "Authorize" no Swagger
3. Cole o token de acesso no formato: `Bearer seu_token_aqui`

---

## 🔑 Autenticação

O sistema usa autenticação **Bearer Token** (JWT):

| Configuração | Valor |
|--------------|-------|
| **Login** | POST `/api/token/` com `cpf` e `senha` |
| **Access Token** | Válido por 30 minutos |
| **Refresh Token** | Válido por 7 dias |
| **Header** | `Authorization: Bearer {seu_token_de_acesso}` |

**⚠️ Importante:** O login é feito via **CPF**, não email.

---

## 📁 Estrutura do Projeto

```
novo_cortex/
├── AppCore/                      # Núcleo da aplicação
│   ├── basics/                   # Models, views, serializers base
│   ├── core/                     # Camadas (Business, Rules, Helpers, State)
│   └── common/                   # Utilitários (emails, textos)
│
├── Auth/                         # Autenticação
│   └── auth/                     # Login, logout, refresh token
│
├── Usuarios/                     # Módulo de Usuários
│   ├── usuario/                  # Model Usuario (login via CPF)
│   ├── conta/                    # Contas de usuário
│   └── usuario_setor/            # Relação usuário-setor
│
├── Perfis/                       # Perfis de usuário
│   ├── aluno/
│   ├── servidor/
│   ├── terceirizado/
│   └── estagiario/
│
├── EstruturaOrganizacional/      # Estrutura do IFPI
│   ├── campus/
│   ├── setor/
│   ├── cargo/
│   ├── empresa/
│   ├── curso/
│   ├── atividade/
│   └── funcao/
│
├── Vinculos/                     # Vínculos institucionais
│   └── matricula/
│
└── BaseDRFApp/                   # Configurações Django
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## 🗃️ Modelos do Domínio

### Hierarquia de Usuários

```
Usuario (Model base - Login via CPF)
   │
   ├── Servidor (OneToOne)
   ├── Terceirizado (OneToOne + FK Empresa)
   ├── Aluno (OneToOne)
   └── Estagiario (OneToOne + FK Empresa + FK Curso)
```

### Principais Modelos

| Modelo | Descrição |
|--------|-----------|
| **Usuario** | Model de autenticação (USERNAME_FIELD='cpf') |
| **Campus** | Campus do IFPI |
| **Setor** | Setores dentro do campus |
| **Atividade** | Atividades dentro de um setor |
| **Funcao** | Funções dentro de uma atividade |
| **Empresa** | Empresas externas (para terceirizados/estagiários) |
| **Cargo** | Cargos institucionais |
| **Matricula** | Carteirinha/matrícula de usuários |
| **UsuarioSetor** | Relação M:N entre Usuario e Setor (com flags `e_responsavel` e `monitor`) |

---

## 📝 Convenções de Código

| Convenção | Padrão |
|-----------|--------|
| **Aspas** | SEMPRE simples (`'texto'`) |
| **Idioma** | Português (variáveis, funções, comentários) |
| **Nomenclatura de Apps** | snake_case minúsculo |
| **Módulos principais** | PascalCase (`AppCore`, `Usuarios`) |
| **Imports** | Organizados (stdlib → Django → DRF → AppCore → apps locais) |
| **Timezone** | America/Fortaleza |
| **Locale** | pt-BR |

---

## 📄 Paginação

| Configuração | Valor |
|--------------|-------|
| **Padrão** | 10 itens por página |
| **Query param** | `?paginacao=25` |
| **Limites** | Mínimo 1, Máximo 100 |

**Exemplos:**
- `/api/usuarios/` → 10 itens
- `/api/usuarios/?paginacao=50` → 50 itens

---

## 📦 Roadmap: Inserção de Usuários em Lote

> **Status:** Funcionalidade planejada, ainda não implementada.

O sistema suportará inserção em lote de usuários via:
- Upload de arquivos Excel (.xlsx)
- Endpoints REST com JSON
- Painel Admin do Django

---

## 📖 Documentação Adicional

Para informações detalhadas sobre a arquitetura e padrões do projeto, consulte:

- `.github/copilot-instructions.md` - Guia completo para desenvolvimento

---

## 🤝 Contribuindo

1. Clone o repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-feature`)
3. Siga as convenções de código do projeto
4. Consulte `.github/copilot-instructions.md` antes de implementar
5. Faça commit das mudanças (`git commit -m 'Add: nova feature'`)
6. Push para o branch (`git push origin feature/nova-feature`)
7. Abra um Pull Request

---

## 🔒 Segurança

- ✅ Autenticação JWT obrigatória (exceto endpoints públicos)
- ✅ Permissões por tipo de usuário
- ✅ Proteção CSRF
- ✅ CORS configurável
- ✅ Validação de senhas (mínimo 8 caracteres, maiúscula, minúscula, número, caractere especial)
- ✅ Auditoria de mudanças (django-simple-history)

---

## 👨‍💻 Autor

**Lucas Soares** (@soareslucas9090)

Desenvolvido para o **IFPI - Campus Floriano**

---

## 📄 Licença

Este projeto é de uso interno do IFPI - Campus Floriano.

---

**Dúvidas?** Consulte a documentação em `.github/copilot-instructions.md`
