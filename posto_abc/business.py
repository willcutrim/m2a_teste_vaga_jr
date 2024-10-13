from posto_abc.models import Posto
from .rules import PostoRules


class PostoAbcBusiness:
    def criar_posto(self, nome):
        posto = PostoRules().rule_posto_existente(nome)
        if posto:
            return False
        
        Posto.objects.create(nome=nome)
        return True