import time


class Passageiro:
    def __init__(self, numero: int, bags: int):
        """
        Descreve um passageiro
        :param numero: Numero de chegada do passageiro
        :param bags: Quantidade de sacos
        """
        self.numero = numero
        self.bags = bags
        self.entrada = time.time()
        self.tempo_espera = None
        self.tempo_atendimento = None
