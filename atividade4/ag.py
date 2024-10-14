import math
import random
import copy
import matplotlib.pyplot as plt # type: ignore
import sys

# Funcao que le o arquivo texto
def leia_cidades():
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


# Funcao que cria a populacao inicial
def criaPopInicial(npop, pop, ncidades):
    aux = []
    for i in range(npop):
        aux = list(range(ncidades))
        random.shuffle(aux)
        pop.append(aux)

    return pop

# Descobre o fitness da funcao
def fitness(npop, pop, ncidades, grafo):
    fit = []
    for i in range (npop):
        distancia = 0
        for j in range (ncidades-1):
            distancia += grafo[pop[i][j]][pop[i][j +1]]
            """ print("Caminho[",pop[i][j], "][" ,pop[i][j +1], "] = ", grafo[pop[i][j]][pop[i][j +1]])
            print("Distancia = ", distancia) """
        distancia += grafo[pop[i][ncidades-1]][pop[i][0]]
        """ print("Caminho[",pop[i][ncidades-1], "][" ,pop[i][0], "] = ", grafo[pop[i][ncidades-1]][pop[i][0]])
        print("Distancia = ", distancia) """
        fit.append(distancia)
    return fit

# Seleciona os pais da proxima geracao pelo método do torneio
def torneio(npop, fit):
    pais = [0] * npop

    pv = 0.9
    i = 0


    #print("Nao entrei")
    
    while i < npop:
        #print("Entrei e estou na execucao: ", i, " de ", npop)
        # Seleciona aleatoriamente 4 numeros
        p1 = random.randint(0, npop-1)
        p2 = random.randint(0, npop-1)
        
        # Se um desse numeros for igual, seleciona outro
        while p1 == p2 :
            p2 = random.randint(0, npop-1)

        # Seleciona os maiores e menores elementos a partir do fitness de cada um
        if fit[p1] > fit[p2]:
            maior = p1
            menor = p2
        else:
            maior = p2
            menor = p1

        # Se o numero aleatorio r for maior que a probabilidade de vitoria,  
        # entao sorteia um novo numero que representara o novo vencedor.
        r = random.random()
        if r > pv:
            vencedor = maior
        else: 
            vencedor = menor
        
        pais[i] = vencedor
        i += 1

    return pais

# Seleciona os pais da próxima geração pelo método da roleta
def roleta(npop, fit):
    pais = []
    
    # Calcula a soma dos inversos dos valores de fitness
    soma = sum(1/f for f in fit)

    # Se a soma das aptidões for zero, selecionar aleatoriamente
    if soma == 0:
        pais = list(range(npop))
    else:
        roleta = [(1/f)/soma for f in fit]
        
        while len(pais) < npop:
            r = random.uniform(0, 1)
            percorre = 0
            for i, p in enumerate(roleta):
                percorre += p
                if r <= percorre:
                    pais.append(i)
                    break
    
    return pais

def esta_no_cruzamento(elemento, cruzamento):
    return 1 if elemento in cruzamento else 0

def cruzamento(npop, pais, pop, ncidades, tx_cruz):
    pop_inter = []

    for i in range(0, npop-1, 2):
        filho_1 = []
        filho_2 = []
        cruz_1 = []
        cruz_2 = []
        fila_1 = []
        fila_2 = []

        # Confere se os elementos serão cruzados ou não
        m  = random.uniform(0, 1)
        if m <= tx_cruz:
            # Sorteia um número para ser o tanto de
            # informação que será combinada entre os pais 
            r1 = random.randint(1, ncidades-2)
            r2 = random.randint(1, ncidades-2)
            while r1 == r2:
                r2 = random.randint(1, ncidades-1)
            if r1 > r2:
                limite_sup = r1
                limite_inf = r2
            else:
                limite_sup = r2
                limite_inf = r1

            # Faz a troca de informação
            for j in range(limite_inf, limite_sup):
                cruz_1.append(pop[pais[i+1]][j])
                cruz_2.append(pop[pais[i]][j])

            # Conserva a informação dos pais
            for j in range(limite_sup, ncidades):
                fila_1.append(pop[pais[i]][j])
                fila_2.append(pop[pais[i+1]][j]) 
            for j in range(limite_inf):
                fila_1.append(pop[pais[i]][j])
                fila_2.append(pop[pais[i+1]][j])
            for j in range(limite_sup-limite_inf):    
                fila_1.append(cruz_2[j])
                fila_2.append(cruz_1[j])

            # Construir o filho 1
            for j in range(ncidades):
                if j == limite_inf + 1:
                    for k in range(limite_sup-limite_inf):    
                        filho_1.append(cruz_1[k])
                if not esta_no_cruzamento(fila_1[j], cruz_1): 
                    if j < limite_inf:
                            filho_1.append(fila_1[j])
                    else:
                            filho_1.append(fila_1[j])

            # Construir o filho 2
            for j in range(ncidades):
                if j == limite_inf + 1:
                    for k in range(limite_sup-limite_inf):    
                        filho_2.append(cruz_2[k])
                if not esta_no_cruzamento(fila_2[j], cruz_2): 
                    if j < limite_inf:
                            filho_2.append(fila_2[j])
                    else:
                            filho_2.append(fila_2[j])

            pop_inter.append(filho_1)
            pop_inter.append(filho_2)
        else:
            pop_inter.append(pop[pais[i]])
            pop_inter.append(pop[pais[i+1]])

    return pop_inter


# Funcao que faz a mutacao para cada alelo do gene
def mutacao(npop, pop, ncidades, tx_mut):
    for i in range(npop):
        for j in range (ncidades):
            r = random.randint(0, 100)
            r = r/100
            if r <= tx_mut:
                troca = random.randint(0,ncidades-1)
                aux = pop[i][j]
                pop[i][j] = pop[i][troca]
                pop[i][troca] = aux
    return pop
    
# Funcao que seleciona o melhor elemento daquela populacao
def elitismo(npop, fit):
    menor = float('inf') 
    idx = 0

    for i in range(npop):
        if fit[i] < menor:
            menor = fit[i]
            idx = i

    return idx

# Funcao que imprime a populacao
def imprimePop(npop, pop, ncidades):
    for i in range(npop):
        for j in range(ncidades):
            print(str(pop[i][j]) + " ", end="")
        print() 
    pass

# Funcao que imprime o grafico
def plota():
    # Pega os resultados dos arquivos e guarda numa variavel
    with open('saida_1.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    resultados_1 = [float(linha.strip()) for linha in linhas]
    
    with open('saida_2.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    resultados_2 = [float(linha.strip()) for linha in linhas]
   
    geracoes = list(range(nger))

    # Plota o grafico
    #plt.plot(geracoes, resultados_1, label = "Roleta",  linestyle='', marker='o', color='red')
    plt.plot(geracoes, resultados_1, label = "Torneio",  linestyle='', marker='.', color='blue')
    plt.plot(geracoes, resultados_2, label = "Roleta",  linestyle='', marker='.', color='red')
    plt.title('Algoritmo Genético')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor resultado')
    plt.grid(True)
    plt.legend()
    plt.show()      

# Funcao principal que comanda o algortimo genetico
def genericAG(npop, nger, ncidades,  pop, grafo, tipo):    
    # Inicia as variaveis
    pop_inter = []
    pais = []
    fit = []
    melhor_elem = []
    tx_mut = 0.01
    tx_cruz = 1

    g = 0

    # Faz o processo para cada geracao
    while g < nger:
        # Compara se a mutação está estagnada, se estiver, aumenta a mutação
        if g > 5:
            contador = 0
            tamanho = len(melhor_elem) - 1
            manteve = melhor_elem[tamanho]
            for i in range(5, 1, -1):
                if manteve == melhor_elem[tamanho-1]:
                    contador += 1
                tamanho -= 1
                manteve = melhor_elem[tamanho]
            if contador == 4:
                tx_mut = 0.1
            else:
                tx_mut = 0.01        

        # Recebe o fitness de cada elemento
        fit = fitness(npop, pop, ncidades,grafo)

        # Cria o vetor de pais
        if tipo == 0:
            pais = torneio(npop, fit)
        else:
            pais = roleta(npop, fit)

        #Cruza a população de pais e faz a mutação
        pop_inter = cruzamento(npop, pais, pop, ncidades, tx_cruz)
        pop_inter = mutacao(npop, pop_inter, ncidades, tx_mut)

        # Recebe o index do elemento de melhor fitness
        idx = elitismo(npop, fit)
        elite = pop[idx] 

        # Copia a populacao intermediaria pra principal
        pop = copy.deepcopy(pop_inter)

        # Substitui o ultimo elemento pela elite
        pop[npop-1] = elite

        g += 1
        
        melhor_elem.append(fit[idx])
        

    return melhor_elem, elite
    


###############################################################################################################################################################

# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 4:
    print("Por favor, informe o tamanho da populacao, o numero de geracoes do arquivo como argumento, o tipo de penalização (0 para branda e 1 para severa) e se deseja imprimir ou nao (1-sim 0-nao).")
    sys.exit()

# Copia os valores pras variaveis
npop = int(sys.argv[1])
nger = int(sys.argv[2])
grafico = int(sys.argv[3])

ncidades, grafo = leia_cidades()

pop = []
pop = criaPopInicial(npop, pop, ncidades)
melhor_ger, melhor_global= genericAG(npop, nger, ncidades, pop, grafo, 0)
melhor = melhor_ger[-1]
m_cidades = melhor_global

with open('saida_1.txt', 'w') as arquivo:
    for elemento in melhor_ger:
        arquivo.write(str(elemento) + "\n")
arquivo.close()

melhor_ger, melhor_global= genericAG(npop, nger, ncidades, pop, grafo, 1)
melhor_2 = melhor_ger[-1] 

with open('saida_2.txt', 'w') as arquivo:
    for elemento in melhor_ger:
        arquivo.write(str(elemento) + "\n")
arquivo.close()
        
if melhor_2 < melhor:
    melhor = melhor_2
    m_cidades = melhor_global


arquivo =  open("saida.txt","w")
for j in range (ncidades):
    arquivo.write(str(m_cidades[j]) + "\n")
arquivo.write("Distancia = " + str(melhor) + "\n")
arquivo.close()

if grafico == 1:
    plota()

