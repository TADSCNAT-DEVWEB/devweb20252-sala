class Clima:
    def __init__(self, temperatura: float, descricao: str):
        self.temperatura = temperatura
        self.descricao = descricao
class Cidade:
    def __init__(self, nome: str):
        self.nome = nome
    def definir_clima(self, clima: Clima):
        self.clima = clima

class ClimaService:
    def __init__(self):
        self.cidades = {}
    
    def inicializar_cidades(self):
        cidade=Cidade(nome="Natal")
        clima=Clima(temperatura=30.0, descricao="Ensolarado")
        cidade.definir_clima(clima)
        self.cidades[cidade.nome] = cidade
        cidade=Cidade(nome="São Paulo")
        clima=Clima(temperatura=20.0, descricao="Nublado")
        cidade.definir_clima(clima)
        self.cidades[cidade.nome] = cidade
        cidade=Cidade(nome="Rio de Janeiro")
        clima=Clima(temperatura=28.0, descricao="Parcialmente nublado")
        cidade.definir_clima(clima)
        self.cidades[cidade.nome] = cidade
        cidade=Cidade(nome="Oslo")
        clima=Clima(temperatura=-3.0 ,descricao="Neve")
        cidade.definir_clima(clima)
        self.cidades[cidade.nome] = cidade

    def obter_cidade(self, nome: str) -> Cidade:
        cidade = self.cidades.get(nome)
        if cidade:
            return cidade
        else:
            return None
