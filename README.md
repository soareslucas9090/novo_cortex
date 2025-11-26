# Base DRF App - Django 5 + DRF 3.16

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

Projeto base modular para desenvolvimento de APIs REST com Django e Django Rest Framework, implementando arquitetura em camadas bem definidas.

## 🎯 Objetivo

Fornecer uma base sólida, profissional e escalável para desenvolvimento de APIs, com separação clara de responsabilidades através de camadas arquiteturais (Business, Rules, Helpers, State).

## ✨ Características

- 🏗️ **Arquitetura em Camadas**: Business, Rules, Helpers e State
- 🔧 **Modular**: Fácil extensão com novos apps
- 📦 **Reutilizável**: Models, mixins e utilitários base
- 🧪 **Testável**: Camadas desacopladas facilitam testes
- 📝 **Bem Documentado**: Exemplos e guias completos
- ⚡ **Produção Ready**: Configurações para desenvolvimento e produção
- 🎨 **Clean Code**: Segue PEP8 e boas práticas Django/DRF

## 🏗️ Estrutura do Projeto

```
base-drf-app/
│
├── AppCore/                    # Módulo principal
│   ├── core/                   # Camadas de arquitetura base
│   │   ├── business.py         # Lógica de negócios
│   │   ├── rules.py            # Regras de validação
│   │   ├── helpers.py          # Queries e utilitários
│   │   ├── state.py            # Máquina de estados
│   │   └── mixins.py           # Integração com models
│   ├── common/                 # Funcionalidades comuns
│   ├── util/                   # Utilitários gerais
│   └── basics/                 # Models e componentes base
│
├── users/                      # App exemplo completo
│   ├── models.py
│   ├── business.py
│   ├── rules.py
│   ├── helpers.py
│   └── admin.py
│
├── auth/                       # Autenticação
├── BaseDRFApp/                 # Configurações Django
├── ARCHITECTURE.md             # Documentação da arquitetura
├── EXAMPLES.py                 # Exemplos de uso
├── IMPROVEMENTS.md             # Sugestões de melhorias
└── create_app.py               # Script para criar novos apps
```

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd base-drf-app

# Crie ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
copy .env.example .env  # Edite conforme necessário

# Execute migrações
python manage.py makemigrations
python manage.py migrate

# Crie superusuário
python manage.py createsuperuser

# Execute o servidor
python manage.py runserver
```

### Criar Novo App

```bash
# Use o script auxiliar
python create_app.py nome_do_app

# Ou manualmente
mkdir nome_do_app
cd nome_do_app
# Crie os arquivos: __init__.py, apps.py, models.py, business.py, rules.py, helpers.py
```

## 📚 Documentação

### Arquitetura em Camadas

#### 1. **Rules** - Regras de Negócio

```python
from AppCore.core.rules import BaseRules

class ProdutoRules(BaseRules):
    def can_create(self) -> bool:
        # Validações antes de criar
        return True
```

#### 2. **Business** - Lógica de Negócio

```python
from AppCore.core.business import BaseBusiness

class ProdutoBusiness(BaseBusiness):
    rules_class = ProdutoRules

    def create(self, **data):
        if not self.rules.can_create():
            raise BusinessException('Não permitido')
        return Produto.objects.create(**data)
```

#### 3. **Helpers** - Queries e Utilitários

```python
from AppCore.core.helpers import BaseHelpers

class ProdutoHelpers(BaseHelpers):
    def get_em_estoque(self):
        return self.get_queryset().filter(quantidade__gt=0)
```

#### 4. **State** - Máquina de Estados

```python
from AppCore.core.state import ModelState, StateMachineBuilder, ModelStateMixin

# Definir estados
class ProdutoState(ModelState):
    field_status_name = 'status'

class ProdutoPendenteState(ProdutoState):
    status_permissions = [STATUS_APROVADO, STATUS_REJEITADO]

    def can_aprovar(self):
        return True

class ProdutoStateBuilder(StateMachineBuilder):
    STATE_MACHINE_CLASSES = {
        STATUS_PENDENTE: ProdutoPendenteState,
        # ...
    }

# Usar no modelo
class Produto(ModelStateMixin, models.Model):
    status = models.IntegerField(choices=CHOICES_STATUS)
    builder_class = ProdutoStateBuilder

    @property
    def state(self):
        return self.get_model_state()

# Usar no business/views
if not produto.state.can_aprovar():
    raise SystemExceptionError('Não pode aprovar')
```

#### 5. **Model** - Integração

```python
from AppCore.core.mixins import LayeredModelMixin

class Produto(LayeredModelMixin, models.Model):
    business_class = ProdutoBusiness
    rules_class = ProdutoRules
    helpers_class = ProdutoHelpers

    # Agora você pode usar:
    # produto.business.create(...)
    # produto.rules.can_update()
    # Produto.get_helpers().get_em_estoque()
```

### Documentação Completa

- 📖 [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- 💡 [EXAMPLES.py](EXAMPLES.py) - Exemplos práticos
- 🚀 [IMPROVEMENTS.md](IMPROVEMENTS.md) - Melhorias e padrões avançados
- 🎯 [AppCore/core/state/INDEX.md](AppCore/core/state/INDEX.md) - **State Pattern (NOVO!)**

## 🔧 Tecnologias

- **Django** 5.2.7 - Framework web
- **DRF** 3.16.1 - REST Framework
- **SimpleJWT** 5.5.1 - Autenticação JWT
- **drf-spectacular** 0.28.0 - Documentação OpenAPI
- **django-filter** 25.1 - Filtragem avançada
- **simple-history** 3.10.1 - Auditoria de mudanças
- **django-cors-headers** 4.9.0 - CORS
- **PostgreSQL** - Banco de dados (suporte a SQLite também)

## 📦 Apps Incluídos

### AppCore.core

Camadas base de arquitetura (Business, Rules, Helpers, State, Mixins).

### AppCore.basics

Models base reutilizáveis:

- `TimeStampedModel` - created_at, updated_at
- `ActiveModel` - is_active
- `SoftDeleteModel` - soft delete
- `BaseModel` - Combinação de todos

### users

Exemplo completo de implementação:

- Model User customizado
- Integração completa com todas as camadas
- Admin configurado
- Exemplos de uso

## 🎓 Conceitos Importantes

### Separação de Responsabilidades

- **Rules**: Valida SE pode fazer algo (retorna bool ou lança exceção)
- **Business**: Orquestra COMO fazer algo (executa operações)
- **Helpers**: Fornece FERRAMENTAS para fazer (queries, utils)
- **State**: Gerencia ESTADOS e transições baseados no campo status

### State Pattern - Novo! 🎉

O módulo **State Pattern** está **100% implementado** e permite controlar permissões e transições de estado através do campo `status` dos modelos.

**Principais recursos:**

- ✅ Controle de permissões por estado
- ✅ Validação de transições
- ✅ Cache automático
- ✅ Classes CSS dinâmicas para UI
- ✅ Totalmente testado (20+ testes)
- ✅ Documentação completa (6 documentos)

**Quick Start:**

```python
# 1. Criar estados
class DocumentoState(ModelState):
    def can_aprovar(self): return False

class DocumentoPendenteState(DocumentoState):
    status_permissions = [STATUS_APROVADO]
    def can_aprovar(self): return True

# 2. Adicionar ao modelo
class Documento(ModelStateMixin, models.Model):
    status = models.IntegerField()
    builder_class = DocumentoStateBuilder

    @property
    def state(self):
        return self.get_model_state()

# 3. Usar
if documento.state.can_aprovar():
    documento.status = STATUS_APROVADO
    documento.save()
```

**Documentação completa:**

- 📚 [Índice Geral](AppCore/core/state/INDEX.md)
- 🚀 [Quick Start](AppCore/core/state/README.md)
- 📖 [Guia de Implementação](AppCore/core/state/IMPLEMENTATION_GUIDE.md)
- 💡 [Exemplos Detalhados](AppCore/core/state/USAGE_EXAMPLES.md)
- 🎨 [Diagramas](AppCore/core/state/DIAGRAMS.md)
- ❓ [FAQ](AppCore/core/state/FAQ.md)

### Boas Práticas

✅ **FAÇA:**

- Use Business para operações CRUD
- Use Rules para validações
- Use Helpers para queries
- Use aspas simples sempre
- Mantenha camadas desacopladas

❌ **NÃO FAÇA:**

- Lógica de negócio em views
- Validações complexas em models
- Queries em Rules
- Aspas duplas

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar testes específicos
pytest users/tests/

# Com cobertura
pytest --cov=.
```

## 📝 Convenções

- **Módulos principais**: Primeira letra maiúscula (`AppCore`)
- **Apps**: Minúsculas (`users`, `auth`)
- **Arquivos**: Minúsculas (`business.py`, `rules.py`)
- **Aspas**: SEMPRE simples (`'texto'`)
- **Imports**: Organizados e absolutos quando possível

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Lucas Soares (@soareslucas9090)

## 🙏 Agradecimentos

Desenvolvido com ❤️ seguindo as melhores práticas de Django 5 e DRF 3.16.

---

**Dúvidas?** Consulte a documentação em `ARCHITECTURE.md` ou os exemplos em `EXAMPLES.py`
