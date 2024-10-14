import math
import random
import copy
import matplotlib.pyplot as plt # type: ignore
import sys

# Funcao que le o arquivo texto
def leiaCidades():
    with open("instancia.txt", 'r') as arquivo:
        linhas = arquivo.readlines()
    
    # Número total de linhas no arquivo
    ncidades = int(len(linhas))
    
    # Inicializa a lista para armazenar o grafo ou matriz
    grafo = []
    
    # Processa cada linha do arquivo
    for i in range(ncidades):
        # Divide a linha em valores e converte para float
        linha = list(map(float, linhas[i].strip().split()))
        # Adiciona a linha à lista grafo
        grafo.append(linha)
    
    arquivo.close()
    
    return ncidades, grafo

def criaFeromonios(ncidades):
    grafo_fero = []
    for _ in range(ncidades):
        linha = []
        for _ in range(ncidades):
            linha.append(1e-16)  # Use um valor suficientemente pequeno, mas ainda representável
        grafo_fero.append(linha)
    return grafo_fero


# Descobre o fitness da funcao
def fitness(caminho, ncidades, grafo):
    distancia = 0
    for i in range (ncidades-1):
        distancia += grafo[caminho[i]][caminho[i+1]]
    distancia += grafo[caminho[ncidades-1]][caminho[0]]
    return distancia

def proxCidade(vizinhos, cidadeAtual, grafo, grafo_fero, alfa, beta):
    total = 0
    roleta = []
    maior = -float('inf')
    p_cidade = 0

    # Calcular o denominador da probabilidade total
    for vizinho in vizinhos:
        fator = 1 / grafo[cidadeAtual][vizinho]
        total += pow(grafo_fero[cidadeAtual][vizinho], alfa) * pow(fator, beta)

    # Calcular a probabilidade para cada vizinho e construir a roleta
    for vizinho in vizinhos:
        fator = 1 / grafo[cidadeAtual][vizinho]
        prob = (pow(grafo_fero[cidadeAtual][vizinho], alfa) * pow(fator, beta)) / total
        roleta.append(prob)

    # Realizar a roleta para selecionar a próxima cidade
    r = random.uniform(0, 1)
    percorre = 0
    for i, p in enumerate(roleta):
        percorre += p
        if r <= percorre:
            return vizinhos[i]  # Retorna a cidade selecionada

def antSystem(ncidades, grafo_fero, caminhos, p, q):
    # Evaporar feromônios em todas as arestas
    for i in range(ncidades):
        for j in range(ncidades):
            grafo_fero[i][j] = (1 - p) * grafo_fero[i][j]
            
    # Adicionar feromônios de acordo com o caminho percorrido
    for i in range(ncidades):
        fit = fitness(caminhos[i], ncidades, grafo)
        for j in range(ncidades - 1):  
            cidade_atual = caminhos[i][j]
            proxima_cidade = caminhos[i][j+1]
            grafo_fero[cidade_atual][proxima_cidade] += q / fit
            grafo_fero[proxima_cidade][cidade_atual] += q / fit  
        
        grafo_fero[caminhos[i][0]][caminhos[i][-1]] += q / fit
        grafo_fero[caminhos[i][-1]][caminhos[i][0]] += q / fit  

    

def antSystemEAS(ncidades, grafo_fero, caminhos, melhor_caminho, p, q, e):
    # Evapora e adiciona o feromonio de todas as formigas
    antSystem(ncidades, grafo_fero, caminhos, p, q)

    # Reforca o melhor feromonio
    fit = fitness(melhor_caminho, ncidades, grafo)
    for j in range(ncidades - 1):  
        cidade_atual = melhor_caminho[j]
        proxima_cidade = melhor_caminho[j+1]
        grafo_fero[cidade_atual][proxima_cidade] += e * q / fit
        grafo_fero[proxima_cidade][cidade_atual] += e * q / fit 

    grafo_fero[melhor_caminho[0]][melhor_caminho[-1]] += q / fit
    grafo_fero[melhor_caminho[-1]][melhor_caminho[0]] += q / fit  

def antSystemBR(ncidades, grafo_fero, caminhos, p, q, w):
    melhores = [(float('inf'), None)] * w  # Lista de tuplas (fitness, caminho)

    # Evapora feromônios em todas as arestas
    for i in range(ncidades):
        for j in range(ncidades):
            grafo_fero[i][j] = (1 - p) * grafo_fero[i][j]

    # Encontra os w melhores caminhos
    for caminho in caminhos:
        fit = fitness(caminho, ncidades, grafo)

        # Se o novo fitness for melhor que o pior dos melhores, insira-o na lista
        if fit < melhores[-1][0]:
            melhores[-1] = (fit, copy.deepcopy(caminho))
            # Ordena para manter os melhores em ordem crescente
            melhores.sort(key=lambda x: x[0])

    # Separa as tuplas em duas listas: melhores fitness e melhores caminhos
    melhores_fitness = [x[0] for x in melhores]
    caminhos_melhores = [x[1] for x in melhores]

    # Adiciona o feromonio dos w melhores
    for i in range(w):
        for j in range(ncidades - 1):
            cidade_atual = caminhos_melhores[i][j]
            proxima_cidade = caminhos_melhores[i][j+1]
            grafo_fero[cidade_atual][proxima_cidade] += i * q / melhores_fitness[i]
            grafo_fero[proxima_cidade][cidade_atual] += i * q / melhores_fitness[i]
        grafo_fero[caminhos[i][0]][caminhos[i][-1]] += q / fit
        grafo_fero[caminhos[i][-1]][caminhos[i][0]] += q / fit  
        

def atualizaFero(ncidades, grafo_fero, caminhos, melhor_caminho, p, q, e, w, tipo):
    if tipo == 1:
        antSystem(ncidades, grafo_fero, caminhos, p, q)
        return
    
    if tipo == 2:
        antSystemEAS(ncidades, grafo_fero, caminhos, melhor_caminho, p, q, e)
        return
    
    if tipo == 3:
        antSystemBR(ncidades, grafo_fero, caminhos, p, q, w)
        return
    
    print("Algo de errado nao esta certo")

# Funcao que imprime o grafico
def plota():
    # Pega os resultados dos arquivos e guarda numa variavel
    with open('saida_1.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    resultados_1 = [float(linha.strip()) for linha in linhas]

    geracoes = list(range(nger))

    # Plota o grafico
    plt.plot(geracoes, resultados_1,  linestyle='', marker='.', color='blue')
    plt.title('Algoritmo Genético')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor resultado')
    plt.grid(True)
    plt.legend()
    plt.show()      

def genericAG(npop, ncidades, nger, grafo, grafo_fero,abordagem):    
    caminhos = []
    melhor_fit = float('inf') 
    melhor_caminho = []
    melhor_elem = []

    # Parâmetros
    alfa = 1
    beta = 5
    p = 0.5
    q = 100
    e = 0.1
    w = 5

    for g in range(nger):     
        #print("Iteracao: ", g)
        #print()
        caminhos = []  # Reseta os caminhos para cada geração
        for formiga in range(npop):
            viagem = 1
            cidade_inicial = random.choice(range(ncidades))
            caminho_formiga = [cidade_inicial]
            list_aux = list(range(ncidades))
            list_aux.remove(cidade_inicial)

            while viagem < ncidades:
                prox_cidade = proxCidade(list_aux, caminho_formiga[-1], grafo, grafo_fero, alfa, beta)
                list_aux.remove(prox_cidade)
                caminho_formiga.append(prox_cidade)
                viagem += 1

            caminhos.append(caminho_formiga)
            fit = fitness(caminho_formiga, ncidades, grafo)

            if fit < melhor_fit:
                melhor_fit = fit
                melhor_caminho = list(caminho_formiga)

        atualizaFero(ncidades, grafo_fero, caminhos, melhor_caminho, p, q, e, w, abordagem)
        melhor_elem.append(melhor_fit)  

    return melhor_elem, melhor_caminho




###############################################################################################################################################################

# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 4:
    print("Por favor, informe o tamanho da populacao, o numero de geracoes do arquivo como argumento, o tipo de penalização (0 para branda e 1 para severa) e se deseja imprimir ou nao (1-sim 0-nao).")
    sys.exit()

# Copia os valores pras variaveis
#npop = int(sys.argv[1])
nger = int(sys.argv[1])
abordagem = int(sys.argv[2])
grafico = float(sys.argv[3])

ncidades, grafo = leiaCidades()

grafo_fero = criaFeromonios(ncidades)

pop = list(range(ncidades))

melhor_ger, melhor_global= genericAG(ncidades, ncidades, nger, grafo, grafo_fero,abordagem)

melhor = melhor_ger[-1]
m_cidades = melhor_global

with open('saida_1.txt', 'w') as arquivo:
    for elemento in melhor_ger:
        arquivo.write(str(elemento) + "\n")
arquivo.close()


arquivo =  open("saida.txt","w")
for j in range (ncidades):
    arquivo.write(str(m_cidades[j]) + "\n")
arquivo.write("Distancia = " + str(melhor) + "\n")
arquivo.close()

if grafico == 1:
    plota()

