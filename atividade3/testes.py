import subprocess
import matplotlib.pyplot as plt
import numpy as np
import sys

def menor_geracao(linhas_1, linhas_2, saida):
    i=0
    # Encontrando o menor valor na segunda saída
    maior = -float('inf')
    for i in range(len(linhas_1)):
        valor = float(linhas_1[i].strip())
        if valor > maior:
            maior = valor
            idx = i
    saida.append(maior)
    saida.append(idx)

    i=0
    # Encontrando o menor valor na segunda saída
    maior = -float('inf')
    for i in range(len(linhas_2)):
        valor = float(linhas_2[i].strip())
        if valor > maior:
            maior = valor
            idx = i
    saida.append(maior)
    saida.append(idx)

    """ i=0
    # Encontrando o menor valor na segunda saída
    maior = -float('inf')
    for i in range(len(linhas_3)):
        valor = float(linhas_3[i].strip())
        if valor > maior:
            maior = valor
            idx = i
    saida.append(maior)
    saida.append(idx) """

    return saida

# Funcao que plota o grafico com os resultados
def plota(ntestes):
    # Cria um vetor com o número de geracoes a partir de 1
    geracoes = list(range(ntestes))

    # Ler o arquivo de texto
    dados = np.loadtxt('saida_testes.txt')

    # Separar cada coluna em um vetor
    melhor_indv_1 = np.sort(dados[:, 1])
    melhor_indv_2 = np.sort(dados[:, 3])
    #melhor_indv_3 = np.sort(dados[:, 5])
    quando_achou = np.sort(dados[:, 1])

    # Plota a curva suavizada
    plt.plot(geracoes, melhor_indv_1, label="Penalização branda", linestyle='', marker='o', color='blue')
    plt.plot(geracoes, melhor_indv_2, label="Penalização severa", linestyle='', marker='*', color='red')
    #plt.plot(geracoes, melhor_indv_3, label="1000 Gerações", linestyle='', marker='.', color='green')
    #plt.plot(geracoes, quando_achou, linestyle='', marker='o', color='red')
    plt.title('Testes no Algoritmo Genético')
    plt.xlabel('Testes')
    #plt.ylim(250, 350)
    plt.ylabel('Melhor indivíduo')
    plt.grid(True)
    plt.legend()
    plt.show()

#######################################################################################
# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 2:
    print("Por favor, informe o numero de testes do arquivo como argumento")
    sys.exit()

# Copia os valores pras variaveis
ntestes = int(sys.argv[1])
""" 
arquivo_ag = "ag.py"
arquivo_testes = open("saida_testes.txt", "w")

for i in range(ntestes):
    saida = []

    subprocess.run(["python", arquivo_ag, "100", "1000", "0"])

    with open('saida_1.txt', 'r') as arquivo:
        linhas_1 = arquivo.readlines()      

    with open('saida_2.txt', 'r') as arquivo:
        linhas_2 = arquivo.readlines()

    #with open('saida_2.txt', 'r') as arquivo:
    #    linhas_2 = arquivo.readlines() 

    saida = menor_geracao(linhas_1, linhas_2, saida)
        
    # Escrevendo os menores valores no arquivo de saída
    arquivo_testes.write("{} {} {} {}\n".format(saida[0], saida[1], saida[2], saida[3]))

arquivo_testes.close() """

plota(ntestes)
