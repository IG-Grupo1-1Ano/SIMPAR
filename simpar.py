from pythonds.basic import Queue

class Passageiro:
    def __init__(self, bag_pass, ciclo_in):
        self.obtem_bag_pass = bag_pass
        self.obtem_ciclo_in = ciclo_in

    def __str__(self):
        return self.__class__.__name__ + '' + str(self.obtem_bag_pass) + ' - ' + str(self.obtem_ciclo_in)

class Balcao:
    def __init__(self, n_balcao, fila, inic_atend, passt_atend, numt_bag, tempt_esp, bag_utemp):
        self.obtem_n_balcao = n_balcao
        self.obtem_fila = fila
        self.muda_inic_atend = inic_atend
        self.incr_passt_atend = passt_atend
        self.muda_numt_bag = numt_bag
        self.muda_tempt_esp = tempt_esp
    def __str__(self):
        return self.__class__.__name__ + 'b-' + str(self.obtem_n_balcao) + 'f-' + str(self.obtem_fila) + 't-' + str(self.muda_tempt_esp)
