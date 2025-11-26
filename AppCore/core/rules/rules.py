"""
Rules Layer - Camada de Regras de Negócio Teóricas

Esta camada é responsável por:
- Validações de regras de negócio
- Retorno de booleanos ou exceções
- Não deve conter lógica de persistência
- Não deve conter lógica de orquestração (isso é do business)

Métodos padrões que toda classe de Rules deve ter:
- return_exception(msg: str): Lança exceção para ser tratada no business
- return_not_allowed(): Retorna False quando regra não é satisfeita
- return_response(msg: str, execute_exception: bool = False): Retorna mensagem negativa
- Métodos can_* para verificar regras específicas
"""
from AppCore.core.exceptions.exceptions import BusinessRuleException

class ModelInstanceRules:
    def __init__(self, object_instance=None):
        self.object_instance = object_instance

    def return_exception(self, message='', details=None):
        """
        Lança uma exceção com a mensagem para ser tratada no business.
        
        Args:
            msg: Mensagem de erro
            
        Raises:
            BaseRuleException: Sempre lança exceção
        """
        raise BusinessRuleException(message, details)

    def return_not_allowed(self):
        """
        Retorna False para indicar que a ação não é permitida.
        
        Returns:
            bool: Sempre retorna False
        """
        return False

    def return_response(self, message='', details=None, execute_exception=False):
        """
        Retorna uma resposta negativa ou lança exceção.
        
        Args:
            msg: Mensagem de erro
            execute_exception: Se True, lança exceção
            
        Returns:
            bool: False se não lançar exceção
            
        Raises:
            BaseRuleException: Se execute_exception for True
        """
        if execute_exception:
            self.return_exception(message, details)
        
        return False
    

