import subprocess
import matplotlib.pyplot as plt
import numpy as np

def menor_geracao(linhas_1, linhas_2, saida):
    i=0
    # Encontrando o menor valor na primeira saída
    menor = float('inf')
    for i in range(len(linhas_1)):
        valor = float(linhas_1[i].strip())
        if valor < menor:
            menor = valor
            idx = i
    saida.append(menor)
    saida.append(idx)

    i=0
    # Encontrando o menor valor na segunda saída
    menor = float('inf')
    for i in range(len(linhas_2)):
        valor = float(linhas_2[i].strip())
        if valor < menor:
            menor = valor
            idx = i
    saida.append(menor)
    saida.append(idx)

    return saida

# Funcao que plota o grafico com os resultados
def plota(n_ger):
    # Cria um vetor com o número de geracoes
    geracoes = list(range(n_ger))

    # Ler o arquivo de texto
    dados = np.loadtxt('saida_testes.txt')

    # Separar cada coluna em um vetor
    resultados_1 = dados[:, 0]
    resultados_2 = dados[:, 2]

    # Plota o grafico
    plt.plot(geracoes, resultados_1, label="Cruzamento BLXA")
    plt.plot(geracoes, resultados_2, label="Cruzamento BLXAB")
    plt.title('Algoritmo Genético')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor resultado')
    plt.grid(True)
    plt.legend()
    plt.show()

#######################################################################################

n_ger = 100

arquivo = "ag.py"
arquivo_testes = open("saida_testes.txt", "w")

for i in range(n_ger):
    saida = []

    subprocess.run(["python", arquivo, "25", "100", "0"])

    with open('saida_a.txt', 'r') as arquivo_a:
        linhas_1 = arquivo_a.readlines()

    with open('saida_ab.txt', 'r') as arquivo_b:
        linhas_2 = arquivo_b.readlines()      

    saida = menor_geracao(linhas_1, linhas_2, saida)

    # Escrevendo os menores valores no arquivo de saída
    arquivo_testes.write("{} {} {} {}\n".format(saida[0], saida[1], saida[2], saida[3]))

arquivo_testes.close()

plota(n_ger)
