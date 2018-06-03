import threading
import time
import random


class Balcao(threading.Thread):
    # Cada minuto de simulacao demora 0.1 segundos reais a passar
    DURACAO_MINUTO = 0.1

    def __init__(self, numero: int, bags_min: int, bags_max: int):
        """
        Prepara um balcao para atender passageiros
        :param numero: Numero do balcao
        :param bags_min: minimo de bagagens despachadas por minuto
        :param bags_max: maximo de bagagens despachadas por minuto
        """
        threading.Thread.__init__(self)

        self.numero = numero
        self.bags_min = bags_min
        self.bags_max = bags_max

        self.fila_lock = threading.RLock()
        self.fila = []
        self.fila_max_size = 0

        self.running_lock = threading.RLock()
        self.running = False
        self.stopping = False
        self.run_inicio = None
        self.run_fim = None

        self.passageiros_atendidos = []

    def run(self):
        """
        Processa os movimentos do balcao, esta funcao nao deve ser chamada directamente, use Balcao.start()
        :return: None
        """

        # Verifica se podemos iniciar o processamento do balcao
        with self.running_lock:
            if self.stopping or self.running:
                raise Exception("Balcao ainda em processamento")

            self.running = True
            self.run_inicio = time.time()
            self.run_fim = None
            self.stopping = False

        while not self.stopping:
            # Verifica se tempos passageiros para atender
            if any(self.fila):
                with self.fila_lock:
                    cur_passageiro = self.fila[0]
            else:
                # Este sleep so funciona quando nao temos fila, de outro modo nao existe interrupcao entre passageiros
                time.sleep(Balcao.DURACAO_MINUTO)
                continue

            # Calcula o tempo que vamos demorar a atender o passageiro
            velocidade_atendimento = random.randint(self.bags_min, self.bags_max)
            tempo_atendimento = cur_passageiro.bags / velocidade_atendimento * Balcao.DURACAO_MINUTO

            # Esperamos pela passagem desse tempo
            time.sleep(tempo_atendimento)

            hora_atendimento = time.time()

            # TODO: Apenas para debug
            minutos = int(tempo_atendimento // Balcao.DURACAO_MINUTO)
            segundos = int(tempo_atendimento % Balcao.DURACAO_MINUTO * 600)
            print("Balcao {:3} atendeu passageiro {:3} com {:3} sacos em {:02d}:{:02d}".format(
                    self.numero,
                    cur_passageiro.numero,
                    cur_passageiro.bags,
                    minutos,
                    segundos
                )
            )
            # TODO: fim de apenas para debug

            # Removemos o passageiro processado da lista de pendentes
            with self.fila_lock:
                self.fila.remove(cur_passageiro)

            # E acrescentamos a lista de processados, depois de colocar os dados do tempo de atendimento
            cur_passageiro.tempo_espera = hora_atendimento - cur_passageiro.entrada - tempo_atendimento
            cur_passageiro.tempo_atendimento = tempo_atendimento
            self.passageiros_atendidos.append(cur_passageiro)

        # Marca o fim do processamento da fila
        with self.running_lock:
            self.running = False
            self.run_fim = time.time()

    def stop(self):
        """
        Encerra o balcao
        :return: None
        """
        with self.running_lock:
            if self.running or self.stopping:
                self.stopping = True
            else:
                raise Exception("Balcao ja parado")

    def adicionar_passageiro(self, passageiro):
        """
        Adiciona um passageiro a fila de espera
        :param passageiro: Passageiro a adicionar
        :return: None
        """
        with self.fila_lock:
            self.fila.append(passageiro)

            # Actualiza o tamanho maximo da fila caso seja necessario
            tamanho_fila = len(self.fila)
            if tamanho_fila > self.fila_max_size:
                self.fila_max_size = tamanho_fila
