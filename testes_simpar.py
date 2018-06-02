# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 14:44:00 2018

@author: bolsa_000
"""

from pythonds import Queue
from random import randint, choice
from shutil import get_terminal_size
import names, pickle

class TreeNode:
    def __init__(self,key,left=None,right=None,parent=None):
        self.key = key
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,lc,rc):
        self.key = key
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def preorder(self):
        print(self.key)
        if self.leftChild:
            self.leftChild.preorder()
        if self.rightChild:
            self.rightChild.preorder()
    
    def inorder(self):
        if self.leftChild:
            self.leftChild.inorder()
        print(str(self.key))
        if self.rightChild:
            self.rightChild.inorder()
    
    def postorder(self):
        if self.leftChild:
            self.leftChild.postorder()
        if self.rightChild:
            self.rightChild.postorder()
        print(self.key)



class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self,key):
        if self.root:
            self._put(key,self.root)
        else:
            self.root = TreeNode(key)
        self.size = self.size + 1

    def _put(self,key,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,currentNode.leftChild)
            else:
                   currentNode.leftChild = TreeNode(key,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                   self._put(key,currentNode.rightChild)
            else:
                   currentNode.rightChild = TreeNode(key,parent=currentNode)

    def __setitem__(self,k):
       self.put(k)

    def get(self,key):
       if self.root:
           res = self._get(key,self.root)
           if res:
                  return res
           else:
                  return None
       else:
           return None

    def _get(self,key,currentNode):
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.leftChild)
       else:
           return self._get(key,currentNode.rightChild)

    def __getitem__(self,key):
       return self.get(key)

    def __contains__(self,key):
       if self._get(key,self.root):
           return True
       else:
           return False

    def delete(self,key):
      if self.size > 1:
         nodeToRemove = self._get(key,self.root)
         if nodeToRemove:
             self.remove(nodeToRemove)
             self.size = self.size-1
         else:
             raise KeyError('Error, key not in tree')
      elif self.size == 1 and self.root.key == key:
         self.root = None
         self.size = self.size - 1
      else:
         raise KeyError('Error, key not in tree')

    def __delitem__(self,key):
       self.delete(key)

    def spliceOut(self):
       if self.isLeaf():
           if self.isLeftChild():
                  self.parent.leftChild = None
           else:
                  self.parent.rightChild = None
       elif self.hasAnyChildren():
           if self.hasLeftChild():
                  if self.isLeftChild():
                     self.parent.leftChild = self.leftChild
                  else:
                     self.parent.rightChild = self.leftChild
                  self.leftChild.parent = self.parent
           else:
                  if self.isLeftChild():
                     self.parent.leftChild = self.rightChild
                  else:
                     self.parent.rightChild = self.rightChild
                  self.rightChild.parent = self.parent

    def findSuccessor(self):
      succ = None
      if self.hasRightChild():
          succ = self.rightChild.findMin()
      else:
          if self.parent:
                 if self.isLeftChild():
                     succ = self.parent
                 else:
                     self.parent.rightChild = None
                     succ = self.parent.findSuccessor()
                     self.parent.rightChild = self
      return succ

    def findMin(self):
      current = self
      while current.hasLeftChild():
          current = current.leftChild
      return current

    def remove(self,currentNode):
         if currentNode.isLeaf(): #leaf
           if currentNode == currentNode.parent.leftChild:
               currentNode.parent.leftChild = None
           else:
               currentNode.parent.rightChild = None
         elif currentNode.hasBothChildren(): #interior
           succ = currentNode.findSuccessor()
           succ.spliceOut()
           currentNode.key = succ.key
           currentNode.payload = succ.payload

         else: # this node has one child
           if currentNode.hasLeftChild():
             if currentNode.isLeftChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.leftChild
             elif currentNode.isRightChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.leftChild
             else:
                 currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
           else:
             if currentNode.isLeftChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.rightChild
             elif currentNode.isRightChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.rightChild
             else:
                 currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)
                 
# *********** O código em baixo vai limpar o ecrã de forma a facilitar a leitura ********** #

def limpa():
    print("\n" * get_terminal_size().lines, end="")


# ********************************* Menu Inicial de Chegada ******************************** #

def menu():
    limpa()
    limpa()
    print("\n")
    print("####### SIMPAR – Simulação de Passageiros em Partida Aérea ########")
    print("\n")
    print("""       2º Semestre - Informática de Gestão
        Selecione os parâmetros da simulação: 
    [1] Número máximo de passageiros
    [2] Número máximo de bagagens permitido por passageiro
    [3] Número de balcões abertos para atendimento
    [4] Ciclos de tempo em que a simulação decorre
    [5] Percentagem de passageiros a encher no primeiro ciclo
    Passageiros: {}   Bagagens: {}   Balcões: {}   Ciclos: {}  Percentagem: {}
    [7] Correr a simulação
    [8] Pesquisa passageiros antendidos
    [99] para saír...""".format(passa, bag, balc, cicl, pench))


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
        # self.atendidos = 0

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

#    def incr_atendidos(self):
#        """
#        Incrementa em 1 o passt_atend - total de passageiros atendidos
#        :return: None
#        """
#
#        self.atendidos += 1

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
        Retorna o balcão como uma string legível para o utilizador
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



#ponto 4.3
def atende_passageiros(tempo, balcoes,listaPass):
    """
    Atende passageiros nos balcões indicados
    :param tempo: Ciclo de simulação
    :param balcoes: Lista de balcões
    :return: Passageiros colocados em fila
    """
    atendidos = 0
    p_nome=''
    for b in balcoes:
        if b.obtem_fila().isEmpty():
            # Sem passageiros a processar
            print('BALCÃO ' + str(b) + ' sem passageiros a processar')
            b.muda_inic_atend(tempo)
            continue

        fila = b.obtem_fila()
        p = fila.items[-1]  # Para ser Fifo, tem de ser desta forma porque Queue.enqueue() acrescenta no inicio da lista
        tempo_atendimento = tempo + b.inic_atend
        ut_bag = p.bag_pass / b.bag_utemp
        if ut_bag < tempo_atendimento:
            tempo_de_espera = tempo - p.ciclo_in
            p_nome=names.get_full_name()
            print("Atendido, {} com {} bagagens no balcão {} com tempo de espera {}".format(
                    p_nome,
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
            atendidos += 1
            listaPass.put(p_nome)

    return atendidos

#ponto 4.4
def apresenta_resultados(balcoes):
    """
    Apresenta os resultados estatísticos finais
    :param balcoes: Lista de balcões
    :return: None
    """
    lista_tmp=[]
    for i in balcoes:
        if i.passt_atend > 0:
            tmp="Balcão {} despachou {} bagagens por ciclo:".format(i.obtem_n_balcao(), i.bag_utemp)
            lista_tmp.append(tmp)
            print (tmp)

            #print("Balcão {} despachou {} bagagens por ciclo:".format(i.obtem_n_balcao(), i.bag_utemp))
            tmp=(
                "{} passageiros atendidos com média de bagagens / passageiro = {}".format(
                    i.passt_atend,
                    round(i.numt_bag / i.passt_atend, 1)
                )
            )
            lista_tmp.append(tmp)
            print(tmp)
            tmp=("Tempo médio de espera = {}".format(round(i.passt_atend / i.inic_atend, 1)))
            lista_tmp.append(tmp)
            print(tmp)
        else:
            tmp=("Balcão {} não atendeu passageiros".format(i.obtem_n_balcao()))
            lista_tmp.append(tmp)
            print(tmp)
    return lista_tmp
#ponto 4.2
def simpar_simula(num_pass, num_bag, num_balcoes, ciclos, p_enche):
    """
    Corre uma simulação
    :param num_pass: o número de passageiros com bagagem previsto para este voo
    :param num_bag: o número máximo de bagagens permitido por passageiro
    :param num_balcoes: o número de balcões abertos para atendimento e despacho de bagagem
    :param ciclos: os ciclos de tempo em que a simulação decorre.
    :param p_enche:  % de passageiros a encher de arranque
    :return: None
    """
    atendidos = 0
    total = num_pass
    balcoes = []
    terco = ciclos / 3
    listaPass = BinarySearchTree()
    for n_balcao in range(1, num_balcoes + 1):  # gera balcões
        balcoes.append(Balcao(n_balcao, num_bag))
    # passageiros iniciais
    enche = int((num_pass * p_enche) / 100)
    for i in range(0, enche):
        for j in balcoes:
            j.obtem_fila().enqueue(Passageiro(randint(1, num_bag), 0))  # aqui tempo é 0
            num_pass -= 1
# mostra_balcoes(balcoes)
    # Ocupar das filas
    for ciclo in range(0, ciclos):

        # Verifica se temos passageiros para criar
        if num_pass > 0:

            for n_balcao in range(1, num_balcoes + 1):  # aqui precorremos todos os balcões para colocar pessoas na fila
                            # Calcula a probabilidade de acrescentar passageiro
                if ciclo <= terco:
                    probabilidade = 100
                elif ciclo <= terco * 2:
                    probabilidade = 80
                else:
                    probabilidade = 60

                temp = randint(0, 100)
                #print('Terço ' + str(terco)+ ' Probabilidade '+str(probabilidade) +' temp '+ str(temp)) #só para perceber como está a funcionar a probabilidade
                if probabilidade >= temp:
                    # Obtem tamanho da fila com menos passageiros
                    fila_mais_curta = min([balcao.obtem_fila().size() for balcao in balcoes])

                    # Obtem apenas os balcões com o tamanha de fila mais curto
                    # (podem por exemplo existir vários balcões com 0 passageiros)
                    balcoes_filas_curtas = [balcao for balcao in balcoes if balcao.obtem_fila().size() == fila_mais_curta]

                    # E escolhemos de forma aleatória qual usamos
                    balcao_pretendido = choice(balcoes_filas_curtas)

                    # Cria passageiro
                    balcao_pretendido.obtem_fila().enqueue(Passageiro(randint(1, num_bag), ciclo + 1))
                    num_pass -= 1
                    #print('criei um passageiro no b ' + str (balcao_pretendido)) #este print é de controle
        print("««« CICLO n.º {} »»»".format(ciclo + 1))

        atendidos = atendidos + atende_passageiros(ciclo + 1, balcoes,listaPass)

        mostra_balcoes(balcoes)
        if atendidos >= total:
            break
    print('ATENDIDOS ' + str(atendidos) + ' total ' + str(total))
    # Esvazear das filas
    print('********************** Fechou a chegada de novos passageiros **********************')
    conta = 0
    esvazia_ciclo = 0
    esvazia = True
    while esvazia == True:
        for balcao in balcoes:  # vamos aos balcões ver se há filas de espera
            if balcao.obtem_fila().isEmpty() == False:  # se a fila não estiver vazia
                conta += 1  # conta é incrementado
        if conta == 0:  # Se não há filas cheias, sai
            esvazia = False
        else:
            esvazia_ciclo += 1
            ciclo += 1  # novo ciclo
            print("««« CICLO ESVAZIA n.º {} »»»".format(ciclo + esvazia_ciclo))
            atende_passageiros(ciclo, balcoes,listaPass)
            conta = 0  # Volta a zero para controlar o próximo ciclo

    #apresenta_resultados(balcoes)
    with open("SimOutput",'wb') as f: 
            pickle.dump(apresenta_resultados(balcoes),f)
            f.close()
    listaPass.root.inorder()
    # menu()

def fazPesquisa():
    #aqui vai pedir o intput da pesquisa
    print('Pesquisa')

if __name__ == "__main__":

    passa = 70
    bag = 4
    balc = 4
    cicl = 10
    pench = randint(0,100)
    invalid = True  # Inicialização da variável de verificação de erro na Escolha
    while invalid==True:
        menu()  # Chamada do Menu
        if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
            print('A opção não é válida')
            invalid = False  # Limpar a variável
        try:
            print("\n")
            escolha = int(input("Escolha uma opção: "))
        except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
            invalid = True
            continue  # Volta ao início do ciclo While

        if escolha == 1:
            limpa()
            limpa()
            # while True:
            if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
                print('A opção não é válida')
                invalid = False
            try:
                a = passa
                aux = int(input("O valor default é " + str(a) + ", indique o novo valor: "))  # display do valor antigo
                print("O valor passou de: " + str(a))
                print("Para: " + str(aux))
                if aux != a:  # se diferente substitui
                    passa = aux
                input()
            except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
                invalid = True
                continue  # Volta ao início do ciclo While

        elif escolha == 2:
            limpa()
            limpa()
            # while True:
            if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
                print('A opção não é válida')
                invalid = False
            try:
                a = bag
                aux = int(
                    input("O valor default é " + str(a) + ", indique o novo valor: "))  # display do valor antigo
                print("O valor passou de: " + str(a))
                print("Para: " + str(aux))
                if aux != a:  # se diferente substitui
                    bag = aux
                input()
            except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
                invalid = True
                continue  # Volta ao início do ciclo While

        elif escolha == 3:
            limpa()
            limpa()
            # while True:
            if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
                print('A opção não é válida')
                invalid = False
            try:
                a = balc
                aux = int(
                    input("O valor default é " + str(a) + ", indique o novo valor: "))  # display do valor antigo
                print("O valor passou de: " + str(a))
                print("Para: " + str(aux))
                if aux != a:  # se diferente substitui
                    balc = aux
                input()
            except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
                invalid = True
                continue  # Volta ao início do ciclo While

        elif escolha == 4:
            limpa()
            limpa()
            # while True:
            if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
                print('A opção não é válida')
                invalid = False
            try:
                a = cicl
                aux = int(
                    input("O valor default é " + str(a) + ", indique o novo valor: "))  # display do valor antigo
                print("O valor passou de: " + str(a))
                print("Para: " + str(aux))
                if aux != a:  # se diferente substitui
                    cicl = aux
                input()
            except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
                invalid = True
                continue  # Volta ao início do ciclo While

        elif escolha == 5:
            limpa()
            limpa()
            # while True:
            if invalid:  # Verificação se o utilizador escolheu uma opção incorrecta
                print('A opção não é válida')
                invalid = False
            try:
                a = pench
                aux = int(
                    input("O valor default é " + str(a) + ", indique o novo valor: "))  # display do valor antigo
                print("O valor passou de: " + str(a))
                print("Para: " + str(aux))
                if aux != a:  # se diferente substitui
                    pench = aux
                input()
            except ValueError:  # Se o Valor não for um inteiro estamos em estado de erro e tentamos novamente
                invalid = True
                continue  # Volta ao início do ciclo While

        elif escolha == 7:
            simpar_simula(passa, bag, balc, cicl, pench)
        elif escolha == 8:
            fazPesquisa()
       
        elif escolha == 99:
            limpa()
            limpa()
            print("...adeus :( ")
            #invalid = False
            #exit  # Finalizar o programa8
            
        else:
            invalid = True
            continue  # Volta ao início do ciclo While
            input('Prima <ENTER> para continuar . . .')