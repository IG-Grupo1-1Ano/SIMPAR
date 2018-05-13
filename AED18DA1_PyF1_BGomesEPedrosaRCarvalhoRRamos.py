from pythonds import Queue
from random import randint, choice


class Passageiro:
    """
    Descreve um passageiro
    """

    def __init__(self, bag_pass, ciclo_in):
        """
        Inicializa um passageiro
        :param bag_pass: número de bagagens do passageiro
        :param ciclo_in: instante em que foi colocado na fila (número do ciclo da simulação)
        """

        self.bag_pass = bag_pass
        self.ciclo_in = ciclo_in

    def obtem_bag_pass(self):
        """
        Devolve o valor de bag_pass
        :return: bag_pass
        """

        return self.bag_pass

    def obtem_ciclo_in(self):
        """
        devolve o valor de ciclo_in
        :return: ciclo_in
        """

        return self.ciclo_in

    def __str__(self):
        """
        Retorna o passageiro como uma string legivel para o utilizador
        Output esperado:
            [b:4 t:2]
        :return: string
        """

        return "[b:{} t:{}]".format(self.obtem_bag_pass(), self.obtem_ciclo_in())


class Balcao:
    """
    Descreve um balcão e a respectiva fila de passageiros
    """

    def __init__(self, n_balcao, num_bag):
        """
        Inicializa um balcão com o número indicado
        :param n_balcao: número do balcão
        :param num_bag: o número máximo de bagagens permitido por passageiro
        """

        self.n_balcao = n_balcao

        self.fila = Queue()
        self.inic_atend = 0
        self.passt_atend = 0
        self.numt_bag = 0
        self.tempt_esp = 0
        self.bag_utemp = randint(1, num_bag)

    def obtem_n_balcao(self):
        """
        Devolve o valor de n_balcao
        :return: n_balcao
        """

        return self.n_balcao

    def obtem_fila(self):
        """
        Devolve o valor da fila
        :return: fila
        """

        return self.fila

    def muda_inic_atend(self, tempo_atendimento):
        """
        Acumula em inic_atend o “valor” do tempo de atendimento do passageiro
        :param tempo_atendimento: tempo de atendimento
        :return: None
        """

        self.inic_atend = tempo_atendimento

    def incr_passt_atend(self):
        """
        Incrementa em 1 o passt_atend - total de passageiros atendidos por este balcão
        :return: None
        """

        self.passt_atend += 1

    def muda_numt_bag(self, passageiro):
        """
        Acumula em numt_bag do balcão, o bag_pass do passageiro quando este termina de ser atendido
        :param passageiro: passageiro processado
        :return: None
        """

        self.numt_bag += passageiro.obtem_bag_pass()

    def muda_tempt_esp(self, tempo_espera):
        """
        Acumula em tempt_esp o “t” tempo de espera do passageiro
        :param tempo_espera: Tempo de espera
        :return: None
        """

        self.tempt_esp += tempo_espera

    def __str__(self):
        """
        Retorna o balcão como uma string legivel para o utilizador
        Output esperado:
            Quando tem passageiros na fila:
                Balcão 2 tempo 2 : - [b:4 t:1] [b:2 t:2] -
            Quando não tem passageiros na fila:
                Balcão 0 tempo 1 : -
        :return: string
        """

        # Formata a lista de passageiros consoante as especificações
        if self.fila.isEmpty():
            str_pass = "-"
        else:
            passageiros_como_str = [str(passageiro) for passageiro in self.fila.items]
            str_pass = "- {} - ".format(" ".join(passageiros_como_str))

        return "Balcão {} tempo {} : {}".format(self.obtem_n_balcao(), self.tempt_esp, str_pass)


def mostra_balcoes(balcoes):
    """
    Mostra os detalhes dos balcoes
    :param balcoes: Lista de balcões
    :return: None
    """

    for balcao in balcoes:
        print(str(balcao))


def atende_passageiros(tempo, balcoes):
    """
    Atende passageiros nos balcões indicados
    :param tempo: Ciclo de simulação
    :param balcoes: Lista de balcões
    :return: Passageiros colocados em fila
    """

    for b in balcoes:
        if b.obtem_fila().isEmpty():
            # Sem passageiros a processar
            b.muda_inic_atend(tempo)
            continue

        fila = b.obtem_fila()
        p = fila.items[-1]  # Para ser Fifo, tem de ser desta forma porque Queue.enqueue() acrescenta no inicio da lista
        tempo_atendimento = tempo + b.inic_atend
        ut_bag = p.bag_pass / b.bag_utemp

        if ut_bag < tempo_atendimento:
            tempo_de_espera = tempo - p.ciclo_in

            print("Atendido passageiro com {} bagagens no balcão {} com tempo de espera {}".format(
                    p.bag_pass,
                    b.obtem_n_balcao(),
                    tempo_de_espera
                )
            )

            b.muda_inic_atend(tempo + 1)
            b.incr_passt_atend()
            b.muda_numt_bag(p)
            b.muda_tempt_esp(tempo_de_espera)
            fila.items.remove(p)


def apresenta_resultados(balcoes):
    """
    Apresenta os resultados estatísticos finais
    :param balcoes: Lista de balcões
    :return: None
    """

    for i in balcoes:
        if i.passt_atend > 0:
            print("Balcão {} despachou {} bagagens por ciclo:".format(i.obtem_n_balcao(), i.bag_utemp))
            print(
                "{} passageiros atendidos com média de bagagens / passageiro = {}".format(
                    i.passt_atend,
                    round(i.numt_bag / i.passt_atend, 1)
                )
            )
            print("Tempo médio de espera = {}".format(round(i.passt_atend / i.inic_atend, 1)))
        else:
            print("Balcão {} não atendeu passageiros".format(i.obtem_n_balcao()))


def simpar_simula(num_pass, num_bag, num_balcoes, ciclos):
    """
    Corre uma simulação
    :param num_pass: o número de passageiros com bagagem previsto para este voo
    :param num_bag: o número máximo de bagagens permitido por passageiro
    :param num_balcoes: o número de balcões abertos para atendimento e despacho de bagagem
    :param ciclos: os ciclos de tempo em que a simulação decorre.
    :return: None
    """

    balcoes = []
    terco = ciclos / 3

    for n_balcao in range(1, num_balcoes + 1): #gera balcões
        balcoes.append(Balcao(n_balcao, num_bag))

    # Ocupar das filas
    for ciclo in range(0, ciclos):
        #print("««« CICLO n.º {} »»»".format(ciclo + 1))

        #atende_passageiros(ciclo, balcoes)

        # Verifica se temos passageiros para criar
        if num_pass > 0:
            # Calcula a probabilidade de acrescentar passageiro
             for n_balcao in range(1, num_balcoes + 1): #aqui precorremos todos os bacções para colocar pessoas na fila
                if ciclo <= terco:
                    probabilidade = 100
                elif ciclo <= terco * 2:
                    probabilidade = 80
                else:
                    probabilidade = 60

                #if probabilidade >= randint(0, 100):
                    # Obtem fila com menos passageiros
                    #balcao_pretendido = sorted(balcoes, key=lambda x: x.obtem_fila().size())[0]
                temp=randint(0, 100)
                print('Probabilidade '+str(probabilidade) +' temp '+ str(temp)) #só para perceber como está a funcionar a probabilidade
                if probabilidade >= temp:
                #if probabilidade >= randint(0, 100):
                    # Obtem tamanho da fila com menos passageiros
                    fila_mais_curta = min([balcao.obtem_fila().size() for balcao in balcoes])

                    # Obtem apenas os balcoes com o tamanha de fila mais curto
                    # (podem por exemplo existir varios balcoes com 0 passageiros)
                    balcoes_filas_curtas = [balcao for balcao in balcoes if balcao.obtem_fila().size() == fila_mais_curta]

                    # E escolhemos de forma aleatoria qual usamos
                    balcao_pretendido = choice(balcoes_filas_curtas)

                    # Cria passageiro
                    balcao_pretendido.obtem_fila().enqueue(Passageiro(randint(1, num_bag), ciclo))
                    num_pass -= 1
                    print('criei um passageiro no b ' + str (balcao_pretendido)) #este prin é de controle
        print("««« CICLO n.º {} »»»".format(ciclo + 1))

        atende_passageiros(ciclo, balcoes)

        mostra_balcoes(balcoes)

    # Vazar das filas
    print('********************** Fechou a chegada de novos passageiros **********************')
    i = ciclos + 1
    for balcao in balcoes: #vamos aos balcões limpar as filhas
        print('BALCOES '+str(balcao)+ 'estado da fila'+ str(balcao.obtem_fila().isEmpty()))
        if balcao.obtem_fila().isEmpty()==False: # se a fila estiver cheia
            #while any(not balcao.obtem_fila().isEmpty() for balcao in balcoes):
            while not balcao.obtem_fila().isEmpty(): # toca a atender os passageiros
                print("««« CICLO ESVAZIA n.º {} »»»".format(i))
                atende_passageiros(i, balcoes)
                i += 1
    #Só para verificar
    for balcao in balcoes:
        print('BALCOES'+str(balcao)+ 'estado da fila'+ str(balcao.obtem_fila().isEmpty()))
    apresenta_resultados(balcoes)


if __name__ == "__main__":
    simpar_simula(100, 4, 4, 10)
