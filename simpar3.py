import curses
from pythonds import Queue
from random import randint


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

    for n_balcao in range(0, num_balcoes):
        balcoes.append(Balcao(n_balcao, num_bag))

    # Ocupar das filas
    for ciclo in range(0, ciclos):
        print("««« CICLO n.º {} »»»".format(ciclo))

        atende_passageiros(ciclo, balcoes)

        # Verifica se tempos passageiros para criar
        if num_pass > 0 and num_balcoes > 0:
            # Calcula a probabilidade de acrescentar passageiro
            if ciclo <= terco:
                probabilidade = 100
            elif ciclo <= terco * 2:
                probabilidade = 80
            else:
                probabilidade = 60

            if probabilidade >= randint(0, 100):
                # Obtem fila com menos passageiros
                balcoes_ordenados = sorted(balcoes, key=lambda x: x.obtem_fila().size())
                balcao_pretendido = balcoes_ordenados[0]

                # Cria passageiro
                balcao_pretendido.obtem_fila().enqueue(Passageiro(randint(1, num_bag), ciclo))
                num_pass -= 1

        mostra_balcoes(balcoes)

    # Vazar das filas
    i = ciclos
    while any(not balcao.obtem_fila().isEmpty() for balcao in balcoes):
        atende_passageiros(i, balcoes)
        i += 1

    apresenta_resultados(balcoes)


def config_menu(valores, descricoes):
    """
    Mostra ao utilizador um menu de configuração da simulação
    :param valores: Valores a obter com o menu
    :param descricoes: Descrições dos valores
    :return: Tuple: [Array com os valores pedidos] e [Indicação de se o user pretende sair]
    """

    screen = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    screen.keypad(1)

    # Variaveis de suporte
    tecla_user = 'a'
    opc = 0
    nr_opcoes = len(valores)
    cor_sel = curses.color_pair(1)
    cor_normal = curses.A_NORMAL
    posicao_valores = max([len(d) for d in descricoes]) + 5

    # Trata o uso do menu até o user estar na opção de "Simular" ou "Sair" e carregar em enter
    while not (opc >= nr_opcoes and (tecla_user == 10)):
        # Constroi o menu
        screen.clear()
        screen.border(0)
        screen.addstr(0, 2, "Simpar", curses.A_STANDOUT)

        # Descrições dos campos e respectivos valores
        for i in range(0, nr_opcoes):
            screen.addstr(2 + i, 2, descricoes[i], cor_normal)
            screen.addstr(2 + i, posicao_valores, str(valores[i]).rjust(10), cor_sel if opc == i else cor_normal)

        screen.addstr(nr_opcoes + 3, 2, "Simular", cor_sel if opc == 4 else cor_normal)
        screen.addstr(nr_opcoes + 5, 2, "Sair", cor_sel if opc == 5 else cor_normal)

        screen.addstr(22, 2, "Escolha uma opcao...", curses.A_BOLD)

        screen.refresh()

        # Reage ao input do utilizador
        tecla_user = screen.getch()
        if tecla_user == 258:
            # User carregou para baixo
            opc += 1
            if opc > nr_opcoes + 1:
                opc = 0
        elif tecla_user == 259:
            # User carregou para cima
            opc -= 1
            if opc < 0:
                opc = nr_opcoes + 1
        elif opc <= nr_opcoes:
            # Se não estamos no "simular" temos de tratar os butões para alterar os valores,
            # impomos um limite de 999999 para os valores
            if 48 <= tecla_user <= 57 and valores[opc] < 999999:
                # Tecla numerica
                valor = tecla_user - 48
                valores[opc] = valores[opc] * 10 + valor
            elif tecla_user == 263 or tecla_user == 127:
                # Backspace
                valores[opc] = int(valores[opc] / 10)

    curses.endwin()
    return valores, opc == nr_opcoes + 1


if __name__ == "__main__":
    sair = False
    descricoes = ["Passageiros", "Bagagens", "Balcões", "Ciclos"]

    # Valores default
    passageiros = 70
    bags = 4
    balcoes = 4
    ciclos = 10

    while not sair:
        resultado, sair = config_menu([passageiros, bags, balcoes, ciclos], descricoes)

        # Guardamos os valores em vez de usar directamente no simpar_simula
        # para servirem de novo default se o user pedir nova simulação
        passageiros = resultado[0]
        bags = resultado[1]
        balcoes = resultado[2]
        ciclos = resultado[3]

        if not sair:
            if bags == 0:
                print("Valor para Bagagens inválido")
            else:
                simpar_simula(passageiros, bags, balcoes, ciclos)

            input("Prima Enter para continuar...")
