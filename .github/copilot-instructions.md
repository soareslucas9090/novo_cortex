# Instruções para AI Coding Agents - Base DRF App

> **Última atualização:** 27 de novembro de 2025

## Arquitetura em Camadas

Este projeto segue uma arquitetura modular de 4 camadas bem definidas. **Cada model deve ter suas próprias classes de camadas** localizadas no mesmo app:

### 1. **Rules** (`rules.py`) - Regras de Negócio Teóricas

- **Responsabilidade**: Validar SE uma ação pode ser executada (retorna `bool` ou lança exceção)
- **Herda de**: `ModelInstanceRules` (AppCore.core.rules)
- **Não deve**: Conter lógica de persistência ou orquestração
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
- **Captura exceções**: Define `exceptions_handled = (AuthorizationException, BusinessRuleException, ValidationException, NotFoundException)`

```python
from AppCore.core.business.business import ModelInstanceBusiness

class ProdutoBusiness(ModelInstanceBusiness):
    def criar_produto(self, **dados):
        # Business orquestra a operação completa
        regras = ProdutoRules()
        if not regras.can_create():
            raise BusinessRuleException('Não pode criar')
        return Produto.objects.create(**dados)
```

### 3. **Helpers** (`helpers.py`) - Queries e Utilitários

- **Responsabilidade**: Fornecer ferramentas (queries customizadas, formatações, utils)
- **Herda de**: `ModelInstanceHelpers` (AppCore.core.helpers)
- **Acesso**: Queries reutilizáveis, transformações de dados

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

### Hierarquia de Herança

```
                    Pessoa
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
    Servidor      Terceirizado     Aluno       Estagiario
        │                             │
   ┌────┴────┐                    Egresso
   │         │
Professor  TecnicoAdministrativo
```

### Modelos e Relacionamentos

| Modelo                    | Descrição                    | Relacionamentos                             |
| ------------------------- | ---------------------------- | ------------------------------------------- |
| **Campus**                | Campus da instituição        | 1:N com Pessoa                              |
| **Empresa**               | Empresa terceirizada         | 1:N com Terceirizado                        |
| **InstituicaoExterna**    | Instituição para estagiários | 1:N com Estagiario                          |
| **Setor**                 | Setor dentro do campus       | 1:N com Funcao                              |
| **Funcao**                | Função dentro de um setor    | 1:N com PessoaFuncao                        |
| **Pessoa**                | Classe base central          | Herança para todos os tipos de pessoa       |
| **Contato**               | Email/telefone da pessoa     | N:1 com Pessoa                              |
| **Endereco**              | Endereço da pessoa           | N:1 com Pessoa                              |
| **Matricula**             | Carteirinha/matrícula        | N:1 com Pessoa                              |
| **PessoaFuncao**          | Tabela associativa           | M:N entre Pessoa e Funcao                   |
| **Servidor**              | Servidor público             | Herda de Pessoa (OneToOne)                  |
| **Professor**             | Professor                    | Herda de Servidor (OneToOne)                |
| **TecnicoAdministrativo** | Técnico Administrativo       | Herda de Servidor (OneToOne)                |
| **Terceirizado**          | Funcionário terceirizado     | Herda de Pessoa, N:1 com Empresa            |
| **Aluno**                 | Aluno matriculado            | Herda de Pessoa (OneToOne)                  |
| **Egresso**               | Ex-aluno formado             | Herda de Aluno (OneToOne)                   |
| **Estagiario**            | Estagiário                   | Herda de Pessoa, N:1 com InstituicaoExterna |

### Apps Sugeridos (Ordem de Criação)

1. **campus** - Model: `Campus` (sem dependências)
2. **empresas** - Models: `Empresa`, `InstituicaoExterna` (sem dependências)
3. **setores** - Models: `Setor`, `Funcao` (sem dependências)
4. **pessoas** - Models: `Pessoa`, `Contato`, `Endereco`, `Matricula`, `PessoaFuncao` (depende de campus, setores)
5. **servidores** - Models: `Servidor`, `Professor`, `TecnicoAdministrativo` (depende de pessoas)
6. **alunos** - Models: `Aluno`, `Egresso` (depende de pessoas)
7. **terceirizados** - Models: `Terceirizado` (depende de pessoas, empresas)
8. **estagiarios** - Models: `Estagiario` (depende de pessoas, empresas)

### Choices Definidos

- **Status genérico**: `STATUS_ATIVO`, `STATUS_INATIVO`
- **Situação do Aluno**: `MATRICULADO`, `TRANCADO`, `FORMADO`, `DESISTENTE`, `TRANSFERIDO`
- **Turno**: `MATUTINO`, `VESPERTINO`, `NOTURNO`, `INTEGRAL`
- **Forma de Ingresso**: `VESTIBULAR`, `ENEM`, `TRANSFERENCIA`, `REINGRESSO`
- **Carga Horária Servidor**: `20h`, `40h`, `DE` (Dedicação Exclusiva)
- **Título Professor**: `GRADUADO`, `ESPECIALISTA`, `MESTRE`, `DOUTOR`, `POS_DOUTOR`
- **Classe Professor**: `D`, `C`, `B`, `A`, `TITULAR`
- **Nível TAE**: `A`, `B`, `C`, `D`, `E`

### Padrão de Herança nos Models

Usamos **OneToOneField com primary_key=True** para herança:

```python
class Servidor(BasicModel):
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='servidor',
        primary_key=True,
    )
    # campos específicos do servidor...

class Professor(BasicModel):
    servidor = models.OneToOneField(
        Servidor,
        on_delete=models.CASCADE,
        related_name='professor',
        primary_key=True,
    )
    # campos específicos do professor...
```

### Exemplos de Funções por Setor (conforme diagrama)

- **Setor de Saúde**: Médico, Enfermeiro, Odontologista
- **Direção**: Diretor de ensino, Diretor geral
- **Coordenações**: Coordenador de TADS, Coordenador de Biologia, Coordenador de Matemática
- **Rádio**: Monitor da Rádio
- **Geral**: Professor
