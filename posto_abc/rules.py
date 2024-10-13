from posto_abc.models import Posto


class PostoRules:
    def posto(self, nome_posto):
        return Posto.objects.filter(nome=nome_posto)

    def _rule_posto_existente(self, nome_posto):
        if self.posto(nome_posto).exists():
            return True
        
        return False


        
