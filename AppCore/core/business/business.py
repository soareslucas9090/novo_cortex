"""
Business Layer - Camada de Negócios Práticos

Esta camada é responsável por:
- Orquestrar operações de negócio
- Tratar exceções lançadas pela camada Rules ou outras camadas
- Executar operações de CRUD com validações
- Coordenar interações entre diferentes componentes
- Processar lógica de negócio complexa

A camada Business:
- Pode chamar Rules para validações
- Pode chamar Helpers para operações auxiliares
- Pode chamar State para transições de estado
- Deve retornar resultados processados ou lançar exceções tratadas
"""
from AppCore.core.exceptions.exceptions import (
    AuthorizationException, BusinessRuleException, ValidationException, NotFoundException
)


class ModelInstanceBusiness:
    exceptions_handled = (AuthorizationException, BusinessRuleException, ValidationException, NotFoundException)
    
    def __init__(self, object_instance=None):
        self.object_instance = object_instance
