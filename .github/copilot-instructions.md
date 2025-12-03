# Instruções para AI Coding Agents - Base DRF App

> **Última atualização:** 2 de dezembro de 2025

ATUALIZE O ARQUIVO .github/copilot-instructions.md sempre que houver mudanças significativas na estrutura, arquitetura ou convenções do projeto.

## Arquitetura em Camadas

Este projeto segue uma arquitetura modular de 4 camadas bem definidas. **Cada model deve ter suas próprias classes de camadas** localizadas no mesmo app.

### ⚠️ PRINCÍPIO FUNDAMENTAL: Views Leves

**SEMPRE prefira implementar lógica nas camadas (Business, Rules, Helpers, State) ao invés de nas views.**

- **Views devem ser "burras"**: Apenas recebem dados, delegam para o Business, e retornam resposta
- **Toda lógica de negócio** vai no `business.py`
- **Toda validação de regras** vai no `rules.py`
- **Toda query/utilitário** vai no `helpers.py`
- **Toda lógica de estado** vai no `state.py`

```python
# ❌ ERRADO - Lógica na view
def do_action_put(self, serializer_data, request):
    for attr, value in serializer_data.items():
        setattr(self.object, attr, value)
    self.object.save()

# ✅ CORRETO - View delega para business
def do_action_put(self, serializer_data, request):
    self.object.business.atualizar_dados(serializer_data)
```

### Hierarquia de Chamadas

```
View (entrada/saída)
  └── Business (orquestração)
        ├── Rules (validações)
        ├── Helpers (queries/utils)
        └── State (transições de estado)
```

**Importante:**

- Views só chamam **Business**
- Business pode chamar **Rules**, **Helpers** e **State**
- Rules, Helpers e State **NÃO** chamam uns aos outros diretamente

### 1. **Rules** (`rules.py`) - Regras de Negócio Teóricas

- **Responsabilidade**: Validar SE uma ação pode ser executada (retorna `bool` ou lança exceção)
- **Herda de**: `ModelInstanceRules` (AppCore.core.rules)
- **Não deve**: Conter lógica de persistência ou orquestração
- **Chamado por**: Business (nunca diretamente pela view)
- **Exemplo**: `UsuarioRules`, `ContaRules`

```python
from AppCore.core.rules.rules import ModelInstanceRules

class ProdutoRules(ModelInstanceRules):
    def can_delete(self):
        if self.object_instance.tem_vendas:
            self.return_exception('Produto com vendas não pode ser excluído')
        return True
```

### 2. **Business** (`business.py`) - Lógica de Negócio Prática

- **Responsabilidade**: Orquestrar COMO fazer operações (CRUD, workflows complexos)
- **Herda de**: `ModelInstanceBusiness` (AppCore.core.business)
- **Pode chamar**: Rules (validações), Helpers (queries), State (transições)
- **Chamado por**: Views (única camada que views podem chamar diretamente)
- **Captura exceções**: Define `exceptions_handled = (AuthorizationException, BusinessRuleException, ValidationException, NotFoundException)`
- **Acesso**: Via `model.business.nome_do_metodo()` após configurar o mixin

```python
from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException

class ProdutoBusiness(ModelInstanceBusiness):
    def criar_produto(self, **dados):
        # Business orquestra a operação completa
        regras = ProdutoRules()
        if not regras.can_create():
            raise BusinessRuleException('Não pode criar')
        return Produto.objects.create(**dados)

    def atualizar_dados(self, dados):
        '''Método padrão para atualização de dados'''
        try:
            for attr, value in dados.items():
                setattr(self.object_instance, attr, value)
            self.object_instance.save()
        except Exception as e:
            raise SystemErrorException('Não foi possível atualizar os dados.')
```

### 3. **Helpers** (`helpers.py`) - Queries e Utilitários

- **Responsabilidade**: Fornecer ferramentas (queries customizadas, formatações, utils)
- **Herda de**: `ModelInstanceHelpers` (AppCore.core.helpers)
- **Acesso**: Queries reutilizáveis, transformações de dados
- **Chamado por**: Business (não pela view diretamente)

```python
from AppCore.core.helpers.helpers import ModelInstanceHelpers

class ProdutoHelpers(ModelInstanceHelpers):
    def deletar_codigos_expirados(self):
        return Produto.objects.filter(validade__lt=timezone.now()).delete()
```

### 4. **State** (`state.py`) - Máquina de Estados ⚠️ FUTURO

- **Campo obrigatório**: `status` (IntegerField com choices)
- **Pattern**: Cada estado do choice é uma classe que herda de uma superclasse base
- **Métodos**: `posso_editar()`, `posso_excluir()`, `posso_ver_detalhes()` (retornam bool)
- **Acesso**: Via `model.state.FUNCAO_EXEMPLO()`
- **Status**: **Não implementado ainda** - aguardar primeiro modelo que precise de máquina de estados

```python
# FUTURO - Exemplo de como será implementado
class DocumentoState:
    def posso_aprovar(self): return False

class DocumentoPendenteState(DocumentoState):
    def posso_aprovar(self): return True

# No modelo
documento.state.posso_aprovar()  # Acessa método do estado atual
```

## Integração com Models

**Use mixins para conectar camadas ao model:**

```python
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin
from AppCore.basics.models.models import BasicModel

class Produto(ModelHelperMixin, ModelBusinessMixin, BasicModel):
    business_class = ProdutoBusiness  # Define a classe de business
    helper_class = ProdutoHelpers     # Define a classe de helpers

    # Acesso via propriedades
    # produto.business.criar_produto(...)
    # produto.helper.deletar_codigos_expirados()
```

## Models e Managers

### Model Base

**Sempre herde de `BasicModel`** para obter:

- `created_at`, `updated_at` (timestamps automáticos)
- `history` (auditoria via django-simple-history)
- Manager customizado que lança `NotFoundException` ao invés de `DoesNotExist`

```python
from AppCore.basics.models.models import BasicModel

class MinhaModel(BasicModel):
    # Seus campos aqui
    pass
```

### Custom Managers

- Crie managers customizados para User models (combine `BaseUserManager` + `Base404ExceptionManager`)
- Todos os managers devem herdar de `Base404ExceptionManager` para lançar `NotFoundException`

## Serializers - Padrão de Montagem

**Serializers devem seguir estas convenções:**

1. **Serializers de Input** (dados recebidos):
   - Use `serializers.Serializer` (não ModelSerializer)
   - Defina `write_only=True` em campos sensíveis
   - Implemente validações customizadas em `validate_<field>()` e `validate()`
2. **Validações de senha**:

   - Mínimo 8 caracteres
   - Pelo menos 1 maiúscula, 1 minúscula, 1 número, 1 caractere especial
   - Use regex para validar: `r'[A-Z]'`, `r'[a-z]'`, `r'\d'`, e caracteres especiais

3. **Validações de código**:
   - Códigos de verificação devem ter exatamente 6 dígitos

```python
from rest_framework import serializers

class CriarContaSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    senha = serializers.CharField(write_only=True)

    def validate_senha(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Senha deve ter pelo menos 8 caracteres.")
        # ... outras validações
        return value
```

## Views - Padrão Básico

**Use as views base de `AppCore.basics.views.basic_views`:**

### BasicPostAPIView

- Para operações POST
- Override `do_action_post(self, serializer, request)`
- Define `mensagem_sucesso` (mensagem padrão de sucesso)
- Retorna dict com `mensagem` e `status_code` (opcional)
- **Transaction automática**: Operação roda dentro de `transaction.atomic()` com savepoint

```python
from AppCore.basics.views.basic_views import BasicPostAPIView

class CriarProdutoView(BasicPostAPIView):
    serializer_class = CriarProdutoSerializer
    mensagem_sucesso = "Produto criado com sucesso."

    def do_action_post(self, serializer, request):
        dados = serializer.validated_data
        ProdutoBusiness().criar_produto(**dados)
        # Retorno opcional para customizar resposta
        return {
            'mensagem': 'Mensagem customizada',
            'status_code': status.HTTP_201_CREATED
        }
```

### Tratamento de Exceções

As views básicas **capturam automaticamente** e retornam HTTP adequado:

- `BusinessRuleException` → 400 Bad Request
- `ValidationException` → 400 Bad Request
- `AuthorizationException` → 403 Forbidden
- `NotFoundException` → 404 Not Found
- `SystemErrorException` → 500 Internal Server Error

## Permissions - Padrão ⚠️ FUTURO

**Sistema de permissões precisa ser padronizado.** Por enquanto, use:

- `AllowAnyMixin` (de `AppCore.basics.mixins.mixins`) para endpoints públicos
- `IsOwnerOrAdminPermission` para endpoints que exigem ser dono ou admin
  - Verifica: `is_superuser` OU perfil tipo `PERFIL_TIPO_ADMIN` ativo OU é o dono do recurso
  - Requer método `obter_usuario_dono(obj)` na view

## Exceções Customizadas

**Sempre use exceções do AppCore** (`AppCore.core.exceptions.exceptions`):

- `BusinessRuleException` - Regra de negócio violada
- `ValidationException` - Dados inválidos
- `AuthorizationException` - Sem permissão
- `NotFoundException` - Objeto não encontrado (auto-lançada pelos managers)
- `SystemErrorException` - Erro interno do sistema

## Convenções de Código

### Estrutura de Apps

```
AppNome/
├── __init__.py
├── apps.py
├── business.py      # Lógica de negócios (opcional)
├── choices.py       # Choices para campos (opcional)
├── rules.py         # Regras de validação (opcional)
├── helpers.py       # Queries e utilitários (opcional)
├── models.py        # Models Django
├── serializers.py   # DRF Serializers
├── state.py         # Classes de estados e máquina de estados (opcional)
├── views.py         # DRF Views
└── urls.py          # URL routing
```

### Estilo de Código

- **Aspas simples**: SEMPRE use `'texto'` (nunca aspas duplas)
- **Imports**: Organizados (stdlib → Django → DRF → AppCore → apps locais)
- **Nomes**:
  - Módulos principais: PascalCase (`AppCore`, `BaseDRFApp`)
  - Apps: snake_case minúsculo (`usuarios`, `auth`)
  - Arquivos: snake_case (`business.py`, `helpers.py`)
- **Nomenclatura em Português**:
  - Variáveis e funções: português (`mensagem_sucesso`, `obter_usuario_dono()`)
  - Estruturas de pastas: `AppCore/common/textos/` (emails, mensagens)
  - Funções utilitárias: `enviar_email_simples()` (não `send_simple_email()`)

### Localização

- Idioma: Português (pt-BR)
- Timezone: `America/Fortaleza`
- Verbose names em português: `verbose_name='Usuário'`

## Comandos Essenciais

### Desenvolvimento

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Rodar servidor
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### Criar Novo App

**Script `create_app.py` está vazio** - criar apps manualmente:

```bash
mkdir NomeApp
cd NomeApp
# Criar: __init__.py, apps.py, models.py, business.py, rules.py, helpers.py, serializers.py, views.py, urls.py
```

## Stack Técnica

- **Django 5.2.7** + **DRF 3.16.1**
- **Auth**: SimpleJWT (tokens com 30min/7dias de validade)
- **Database**: PostgreSQL (dev usa SQLite)
- **Docs API**: drf-spectacular (Swagger/ReDoc em `/api/schema/swagger/`)
- **Auditoria**: django-simple-history (histórico automático em models)
- **Email**: SMTP (padrão Gmail, configurável via env)

## Paginação

O projeto usa uma classe de paginação customizada (`AppCore.basics.pagination.pagination.PaginacaoCustomizada`):

- **Tamanho padrão**: 10 itens por página
- **Query param**: `paginacao` - permite definir o tamanho da página dinamicamente
- **Limites**: Mínimo 1, Máximo 100
  - Valores menores que 1 são ajustados para 1
  - Valores maiores que 100 são ajustados para 100

```python
# Exemplos de uso:
# /api/usuarios/              → 10 itens (padrão)
# /api/usuarios/?paginacao=25 → 25 itens
# /api/usuarios/?paginacao=0  → 1 item (mínimo)
# /api/usuarios/?paginacao=500 → 100 itens (máximo)
```

## Documentação da API (Swagger/OpenAPI)

**OBRIGATÓRIO**: Toda view deve ter documentação completa usando `drf-spectacular`.

### Decorador @extend_schema

Sempre adicione o decorador `@extend_schema` em todas as views:

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    tags=['NomeDoModulo'],
    summary='Descrição curta da operação',
    description='''
    Descrição detalhada da operação.

    **Permissões:** Quem pode acessar
    **Paginação:** Informações sobre paginação (se aplicável)

    **Retorno:**
    - Lista dos campos retornados
    ''',
    request=SerializerDeInput,  # Para POST/PUT
    responses={
        status.HTTP_200_OK: SerializerDeOutput,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão'},
        status.HTTP_404_NOT_FOUND: {'description': 'Não encontrado'},
    },
    examples=[  # Opcional, mas recomendado
        OpenApiExample(
            'Exemplo de Requisição',
            value={'campo': 'valor'},
            request_only=True,
        ),
    ],
)
class MinhaView(BasicGetAPIView):
    ...
```

### Padrões de Tags

Use tags consistentes para agrupar endpoints no Swagger:

- `Auth` - Autenticação e tokens
- `Usuarios` - Operações de usuários
- `Usuarios.Password reset` - Reset de senha
- `Campus`, `Setores`, `Empresas`, etc. - Entidades do domínio

### Serializers para Documentação

Para endpoints de input (POST/PUT), crie serializers separados quando necessário:

- `SerializerInput` - Para documentar o request body
- `SerializerResponse` - Para documentar a resposta

Veja exemplo em `Auth.auth.serializers` com `LoginInputSerializer` e `LoginResponseSerializer`.

## URLs e Estrutura de Rotas

- Apps agrupam URLs: `path('usuarios/', include('Usuarios.urls'))`
- Apps compostos (Usuarios, Auth) têm `urls.py` na raiz que inclui sub-apps
- Documentação: `/api/schema/`, `/api/schema/swagger/`, `/api/schema/redoc/`

## Testing

**Por enquanto o projeto não terá testes** - foco em implementação.

## Deploy (Futuro)

**Planejado mas não configurado**:

- Deploy com Docker
- Server: Gunicorn (Linux) / Waitress (Windows)
- Static files: WhiteNoise (já configurado)

---

## Modelos do Domínio (DER/Diagrama de Classes)

O arquivo `Usuarios/models-teste.py` contém a tradução completa do DER para Django Models. Abaixo está o resumo dos modelos e seus relacionamentos:

### Autenticação

- **Login por CPF** (não email)
- **Criação de usuários**: Via JSON por admin (individual ou em lote) ou por portal Admin
- **Não há auto-cadastro**: Usuários são criados por administradores

### Hierarquia de Herança

```
                    Usuario
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
    Servidor      Terceirizado     Aluno       Estagiario
```

### Modelos e Relacionamentos

| Modelo           | Descrição                       | Relacionamentos                                           |
| ---------------- | ------------------------------- | --------------------------------------------------------- |
| **Campus**       | Campus da instituição           | 1:N com Usuario                                           |
| **Cargo**        | Cargos na instituição           | Entidade independente                                     |
| **Empresa**      | Empresa/Instituição externa     | 1:N com Terceirizado, 1:N com Estagiario                  |
| **Curso**        | Cursos para estagiários         | 1:N com Estagiario                                        |
| **Setor**        | Setor dentro do campus          | 1:N com Atividade, M:N com Usuario (via UsuarioSetor)     |
| **Atividade**    | Atividade dentro de um setor    | 1:N com Funcao                                            |
| **Funcao**       | Função dentro de uma atividade  | N:1 com Atividade                                         |
| **Usuario**      | Classe base central (login CPF) | Herança para todos os tipos, 1:N com Contato/Endereco/etc |
| **UsuarioSetor** | Tabela associativa              | M:N entre Usuario e Setor (com e_responsavel, monitor)    |
| **Contato**      | Email/telefone do usuário       | N:1 com Usuario                                           |
| **Endereco**     | Endereço do usuário             | N:1 com Usuario                                           |
| **Matricula**    | Carteirinha/matrícula           | N:1 com Usuario                                           |
| **Servidor**     | Servidor público                | Herda de Usuario (OneToOne)                               |
| **Terceirizado** | Funcionário terceirizado        | Herda de Usuario, N:1 com Empresa                         |
| **Aluno**        | Aluno matriculado               | Herda de Usuario (OneToOne)                               |
| **Estagiario**   | Estagiário                      | Herda de Usuario, N:1 com Empresa, N:1 com Curso          |

### Apps Sugeridos (Ordem de Criação)

1. **campus** - Model: `Campus` (sem dependências)
2. **cargos** - Model: `Cargo` (sem dependências)
3. **empresas** - Models: `Empresa`, `Curso` (sem dependências)
4. **usuarios** - Models: `Usuario`, `Contato`, `Endereco`, `Matricula` (depende de campus)
5. **setores** - Models: `Setor`, `Atividade`, `Funcao`, `UsuarioSetor` (depende de usuarios, campus)
6. **servidores** - Model: `Servidor` (depende de usuarios)
7. **alunos** - Model: `Aluno` (depende de usuarios)
8. **terceirizados** - Model: `Terceirizado` (depende de usuarios, empresas)
9. **estagiarios** - Model: `Estagiario` (depende de usuarios, empresas)

### Choices Definidos

- **Status genérico**: `STATUS_ATIVO`, `STATUS_INATIVO`
- **Situação do Aluno**: `MATRICULADO`, `TRANCADO`, `FORMADO`, `DESISTENTE`, `TRANSFERIDO`
- **Turno**: `MATUTINO`, `VESPERTINO`, `NOTURNO`, `INTEGRAL`
- **Forma de Ingresso**: `VESTIBULAR`, `ENEM`, `TRANSFERENCIA`, `REINGRESSO`
- **Jornada de Trabalho Servidor**: `20`, `40`, `0` (Dedicação Exclusiva)

### Padrão de Herança nos Models

Usamos **OneToOneField com primary_key=True** para herança:

```python
class Servidor(BasicModel):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='servidor',
        primary_key=True,
    )
    # campos específicos do servidor...

class Aluno(BasicModel):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='aluno',
        primary_key=True,
    )
    # campos específicos do aluno...
```

### Usuario - Configuração de Autenticação

```python
class Usuario(AbstractBaseUser, BasicModel):
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome']

    # campos...
    cpf = models.CharField('CPF', max_length=11, unique=True)
    nome = models.CharField('Nome', max_length=255)
    # ...
```

### UsuarioSetor - Tabela Associativa

```python
class UsuarioSetor(BasicModel):
    usuario = models.ForeignKey(Usuario, ...)
    setor = models.ForeignKey(Setor, ...)
    campus = models.ForeignKey(Campus, ...)
    e_responsavel = models.BooleanField(default=False)
    monitor = models.BooleanField(default=False)
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True)
```

### Criação de Usuários (Via Admin JSON)

- Usuários são criados por administradores via endpoint específico
- Suporte a criação individual ou em lote via JSON
- Não há fluxo de auto-cadastro com envio de email
