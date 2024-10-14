import subprocess
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import sys

def menor_geracao(linhas_1, linhas_2, linhas_3, saida):
    i=0
    # Encontrando o menor valor na segunda saída
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

    i=0
    # Encontrando o menor valor na segunda saída
    menor = float('inf')
    for i in range(len(linhas_3)):
        valor = float(linhas_3[i].strip())
        if valor < menor:
            menor = valor
            idx = i
    saida.append(menor)
    saida.append(idx)

    return saida

# Funcao que plota o grafico com os resultados
def plota(ntestes):
    # Cria um vetor com o número de geracoes a partir de 1
    geracoes = list(range(ntestes))

    # Ler o arquivo de texto
    dados = np.loadtxt('saida_testes.txt')

    # Separar cada coluna em um vetor
    melhor_indv_1 = np.sort(dados[:, 0])
    melhor_indv_2 = np.sort(dados[:, 2])
    melhor_indv_3 = np.sort(dados[:, 4])
    quando_achou = np.sort(dados[:, 1])

    media_valores_1 = np.mean(melhor_indv_1)
    media_valores_2 = np.mean(melhor_indv_2)
    media_valores_3 = np.mean(melhor_indv_3)

    # Plota a curva suavizada
    plt.plot(geracoes, melhor_indv_1, label="Padrão", linestyle='', marker='o', color='blue')
    plt.plot(geracoes, melhor_indv_2, label="EAS", linestyle='', marker='*', color='red')
    plt.plot(geracoes, melhor_indv_3, label="Best Ranked", linestyle='', marker='.', color='green')
    #plt.plot(geracoes, quando_achou, linestyle='', marker='o', color='red')
    plt.axhline(y=media_valores_1, color='blue', linestyle='-', label=f'Média do padrão = 5: {media_valores_1:.0f}')
    plt.axhline(y=media_valores_2, color='red', linestyle='-', label=f'Média do EAS = 10: {media_valores_2:.0f}')
    plt.axhline(y=media_valores_3, color='green', linestyle='-', label=f'Média do Best Ranked: {media_valores_3:.0f}')
    plt.title('Testes no Algoritmo Genético')
    plt.xlabel('Testes')
    #plt.ylim(250, 350)
    plt.ylabel('Melhor Indivíduo')
    #plt.ylabel('N° Gerações')
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
    print("TESTE: ", i)
    
    saida = []

    subprocess.run(["python", arquivo_ag, "100", "0", "1"])

    with open('saida_1.txt', 'r') as arquivo:
        linhas_1 = arquivo.readlines()   

    subprocess.run(["python", arquivo_ag, "100", "0", "2"])

    with open('saida_1.txt', 'r') as arquivo:
        linhas_2 = arquivo.readlines()   
    
    subprocess.run(["python", arquivo_ag, "100", "0", "3"])

    with open('saida_1.txt', 'r') as arquivo:
        linhas_3 = arquivo.readlines()

    saida = menor_geracao(linhas_1, linhas_2, linhas_3, saida)
        
    # Escrevendo os menores valores no arquivo de saída
    arquivo_testes.write("{} {} {} {} {} {}\n".format(saida[0], saida[1], saida[2], saida[3], saida[4], saida[5]))

arquivo_testes.close()
 """
plota(ntestes)
