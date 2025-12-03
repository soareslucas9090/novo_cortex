from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException


class EstagiarioBusiness(ModelInstanceBusiness):
    """
    Classe de business para operações relacionadas a Estagiario.
    
    Responsável por orquestrar as operações de CRUD e
    lógica de negócio prática do modelo Estagiario.
    """
    
    def atualizar_dados(self, dados):
        """
        Atualiza os dados de um estagiário existente.
        
        Args:
            dados: Dicionário com os campos a serem atualizados
        
        Raises:
            SystemErrorException: Se ocorrer erro na atualização
        """
        try:
            for attr, value in dados.items():
                setattr(self.object_instance, attr, value)
            
            self.object_instance.save()
        except Exception as e:
            raise SystemErrorException('Não foi possível atualizar os dados do estagiário.')

    def deletar_dados(self):
        """
        Realiza a deleção do estagiário.
        
        Como o estagiário não tem campo ativo próprio, a deleção
        é feita através do usuário base.
        
        Raises:
            SystemErrorException: Se ocorrer erro na deleção
        """
        try:
            self.object_instance.usuario.ativo = False
            self.object_instance.usuario.save()
        except Exception as e:
            raise SystemErrorException('Não foi possível deletar o estagiário.')
