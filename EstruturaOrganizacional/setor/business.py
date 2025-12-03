from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException


class SetorBusiness(ModelInstanceBusiness):
    def atualizar_dados(self, dados):
        try:
            for attr, value in dados.items():
                setattr(self.object_instance, attr, value)

            self.object_instance.save()
        except Exception as e:
            raise SystemErrorException('Não foi possível atualizar os dados do setor.')

    def deletar_dados(self):
        try:
            self.object_instance.ativo = False
            self.object_instance.save()
        except Exception as e:
            raise SystemErrorException('Não foi possível deletar o setor.')
