#!/usr/bin/env python3

import Models
import time
import random
from statistics import mean

balcoes = []
balcoes_max = 4
balcoes_bags_min = 1
balcoes_bags_max = 4

passageiros_max = 50
passageiros_bags_min = 1
passageiros_bags_max = 20

# Cria os balcoes
for balcao_nr in range(1, balcoes_max + 1):
    balcao = Models.Balcao(
            balcao_nr,
            balcoes_bags_min,
            # O maximo de bags processado e aleatorio para cada balcao, dentro dos limites definidos
            random.randint(balcoes_bags_min, balcoes_bags_max)
        )

    balcoes.append(balcao)

# Inicia o processamento das filas
for balcao in balcoes:
    balcao.start()

# Acrescenta passageiros as filas
for balcao_nr in range(1, passageiros_max + 1):
    # Obtem tamanho da fila com menos passageiros
    fila_mais_curta = min([len(balcao.fila) for balcao in balcoes])

    # Obtem apenas os balcoes com o tamanha de fila mais curto
    # (podem por exemplo existir varios balcoes com 0 passageiros)
    balcoes_filas_curtas = [balcao for balcao in balcoes if len(balcao.fila) == fila_mais_curta]

    # Escolhemos de forma aleatoria qual usamos
    balcao_escolhido = random.choice(balcoes_filas_curtas)

    # E por fim acrescentamos o passageiro ao balcao
    balcao_escolhido.adicionar_passageiro(
        Models.Passageiro(balcao_nr, random.randint(passageiros_bags_min, passageiros_bags_max))
    )

    # TODO: Colocar uma melhor distribuicao de passageiros no tempo
    time.sleep(random.random() / 4)

# Aguarda pelo fim do processamento
for balcao in balcoes:
    while any(balcao.fila):
        time.sleep(1)

# Para os balcoes
for balcao in balcoes:
    balcao.stop()

# Aguarda pela paragem dos balcoes
for balcao in balcoes:
    while balcao.running:
        time.sleep(1)

# Mostra um relatorio
print("Relatorio")
for balcao in balcoes:
    print("Balcao {:3}:".format(balcao.numero))

    # Medias e tempos
    media_espera = mean([passageiro.tempo_espera for passageiro in balcao.passageiros_atendidos])
    minutos_espera = int(media_espera // Models.Balcao.DURACAO_MINUTO)
    segundos_espera = int(media_espera % Models.Balcao.DURACAO_MINUTO * 600)

    media_atendimento = mean([passageiro.tempo_atendimento for passageiro in balcao.passageiros_atendidos])
    minutos_atendimento = int(media_atendimento // Models.Balcao.DURACAO_MINUTO)
    segundos_atendimento = int(media_atendimento % Models.Balcao.DURACAO_MINUTO * 600)

    print("    Fila: tamanho maximo {:3}".format(balcao.fila_max_size))

    # Dados dos passageiros
    print(
        "    Passageiros: atendidos {:3}, tempo medio de espera {:03d}:{:02d}, tempo medio de atendimento {:02d}:{:02d}"
        .format(
            len(balcao.passageiros_atendidos),
            minutos_espera,
            segundos_espera,
            minutos_atendimento,
            segundos_atendimento
        )
    )

    print(
        "    Sacos: total {:4}, minimo {:2}, maximo {:2}, media {:2.2f}"
        .format(
            sum(passageiro.bags for passageiro in balcao.passageiros_atendidos),
            min(passageiro.bags for passageiro in balcao.passageiros_atendidos),
            max(passageiro.bags for passageiro in balcao.passageiros_atendidos),
            mean(passageiro.bags for passageiro in balcao.passageiros_atendidos)
        )
    )

    # Lista de passageiros
    print("    Lista passageiros:")
    for passageiro in balcao.passageiros_atendidos:
        minutos_espera = int(passageiro.tempo_espera // Models.Balcao.DURACAO_MINUTO)
        segundos_espera = int(passageiro.tempo_espera % Models.Balcao.DURACAO_MINUTO * 600)

        minutos_atendimento = int(passageiro.tempo_atendimento // Models.Balcao.DURACAO_MINUTO)
        segundos_atendimento = int(passageiro.tempo_atendimento % Models.Balcao.DURACAO_MINUTO * 600)
        print(
            "         Passageiro {:3} com {:3} sacos, esperou {:03d}:{:02d}, foi atendido em {:02d}:{:02d}"
            .format(
                passageiro.numero,
                passageiro.bags,
                minutos_espera,
                segundos_espera,
                minutos_atendimento,
                segundos_atendimento
            )
        )
