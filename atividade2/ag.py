import random
import math
import copy
import matplotlib.pyplot as plt
import sys

# Funcao que cria a populacao inicial
def criaPopInicial(npop, pop):
    for i in range(npop):
        aux = []
        for j in range(3):
            aux.append(random.uniform(-2,2))
        pop.append(aux)

    return pop


# Descobre o fitness da funcao
def avaliaPop(npop, pop):

    fit = []

    for i in range (npop):

        somatorio_1 = pop[i][0]**2 + pop[i][1]**2 + pop[i][2]**2

        somatorio_2 = math.cos(2* math.pi * pop[i][0]) + math.cos(2* math.pi * pop[i][1]) + math.cos(2* math.pi * pop[i][2])

        elevado_1 = 1/3 * somatorio_2

        elevado_2 = -0.2*(math.sqrt(1/3 * somatorio_1)) 

        fit.append(-20*math.exp(elevado_2) - math.exp(elevado_1) + 20 + math.exp(1))
    
    return fit

# Seleciona os pais da proxima geracao
def torneio(npop, fit):
    pais = []
    aux_fit = []
    roleta = [] 
    soma = 0

    for i in range (npop):
        aux_fit.append (1/fit[i])
        soma += aux_fit[i]

    for i in range (npop):
        roleta.append(aux_fit[i]/soma)


    while len(pais) != npop:
        r = random.uniform(0,1)
        percorre = 0
        j = 0
        
        while True:
            percorre += roleta[j]
            if r <= percorre:
                pais.append(j)
                break
        
            j+=1

    return pais


# Funcao que faz  o cruzamento entre os pais
def cruzamento_blxa(npop, pais, pop):
    filhos = []
    alfa = 0.5

    # Se npop for ímpar, exclua o último indivíduo da iteração do loop
    if npop % 2 != 0:
        tamanho = npop- 1
    else:
        tamanho = npop

    for i in range (0,tamanho,2):
        aux_filho_1 = []
        aux_filho_2 = []

        for j in range (3):
            d = abs(pop[pais[i]][j] - pop[pais[i+1]][j])
            intervalo_1 = min(pop[pais[i]][j], pop[pais[i+1]][j] + alfa * d)
            intervalo_2 = max(pop[pais[i]][j], pop[pais[i+1]][j] + alfa * d)

            #filho 1
            aux_filho_1.append(random.uniform(intervalo_1, intervalo_2))

            #filho 2
            aux_filho_2.append(random.uniform(intervalo_1, intervalo_2))
    
        filhos.append(aux_filho_1)
        filhos.append(aux_filho_2)

    # Se npop for ímpar, adicione o último indivíduo ao final da lista de filhos
    if npop % 2 != 0:
        aux_filho_1 = copy.deepcopy(pop[pais[i]])
        filhos.append(aux_filho_1)

    return filhos

# Funcao que faz  o cruzamento entre os pais
def cruzamento_blxab(npop, pais, pop):
    filhos = []
    alfa = 0.75
    beta = 0.25

    # Se npop for ímpar, exclua o último indivíduo da iteração do loop
    if npop % 2 != 0:
        tamanho = npop- 1
    else:
        tamanho = npop

    for i in range(0, tamanho, 2):
        aux_filho_1 = []
        aux_filho_2 = []

        for j in range(3):
            d = abs(pop[pais[i]][j] - pop[pais[i+1]][j])

            if pop[pais[i]][j] - pop[pais[i+1]][j]:
                aux_filho_1.append(random.uniform(pop[pais[i]][j] - alfa * d, pop[pais[i+1]][j] + beta * d))
                aux_filho_2.append(random.uniform(pop[pais[i]][j] - alfa * d, pop[pais[i+1]][j] + beta * d))
            else:
                aux_filho_1.append(random.uniform(pop[pais[i+1]][j] - alfa * d, pop[pais[i]][j] + beta * d))
                aux_filho_2.append(random.uniform(pop[pais[i+1]][j] - alfa * d, pop[pais[i]][j] + beta * d))
        
        filhos.append(aux_filho_1)
        filhos.append(aux_filho_2)

    # Se npop for ímpar, adicione o último indivíduo ao final da lista de filhos
    if npop % 2 != 0:
        aux_filho_1 = copy.deepcopy(pop[pais[i]])
        filhos.append(aux_filho_1)

    return filhos



# Funcao que faz a mutacao para cada alelo do gene
def mutacao(npop, pop):
    tx_mutacao = 0.1
    for i in range(npop):
        for j in range(3):
            r = random.uniform(0, 1)
            if r <= tx_mutacao:
                pop[i][j] = random.uniform(-2, 2)
    return pop

    
# Funcao que seleciona o melhor elemento daquela populacao
def elitismo(npop, fit):
    menor = float('inf') 
    idx = 0

    for i in range(npop -1, -1, -1):
        if fit[i] < menor:
            menor = fit[i]
            idx = i

    return idx

# Funcao que imprime a populacao
def imprimePop(npop, pop):
    for i in range(npop):
        for j in range(3):
            print(str(pop[i][j]) + " ", end="")
        print() 
    pass

# Funcao que plota o grafico com os resultados dos dois metodos
def plota(n_ger):
    # Le os arquivos e guarda eles nas variaveis 'linhas'
    with open('saida_a.txt', 'r') as arquivo:
        linhas_1 = arquivo.readlines()

    with open('saida_ab.txt', 'r') as arquivo:
        linhas_2 = arquivo.readlines()

    resultados_1 = [float(linha.strip()) for linha in linhas_1]
    resultados_2 = [float(linha.strip()) for linha in linhas_2]

    geracoes = list(range(n_ger))

    # Plota o grafico
    plt.plot(geracoes, resultados_1, label = "Cruzamento BLXA")
    plt.plot(geracoes, resultados_2, label = "Cruzamento BLXAB")
    plt.title('Algoritmo Genético')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor resultado')
    plt.grid(True)
    plt.legend() 
    plt.show()


# Funcao principal que comanda o algortimo genetico
def genericAG(n_pop, pop, n_ger, tipo):
    arquivo =  open("saida_a.txt","w")
    
    # Inicia as variaveis
    filhos = []
    pais = []
    fit = []
    tx_cruz = 1

    g = 0

    # Faz o processo para cada geracao
    while g < n_ger:
        fit = avaliaPop(n_pop, pop)
        pais = torneio(n_pop, fit)
        
        # Pega um valor aleatorio de 0 a 1 e se for menor que a taxa de cruzamento,
        # O cruzamento é feito, do contrário, ele é ignorado
        r = random. uniform(0,1)
        if r < tx_cruz:
            if tipo == 0:
                filhos = cruzamento_blxa(n_pop, pais, pop)
            else:
                filhos = cruzamento_blxab(n_pop, pais, pop)
        else:
            filhos = copy.deepcopy(pop)

        filhos = mutacao(n_pop, filhos)


        # Recebe o index do elemento de melhor fitness
        idx = elitismo(n_pop, fit)
        elite = pop[idx] 


        # Copia a populacao intermediaria pra principal
        if r < tx_cruz:
            pop = copy.deepcopy(filhos)

        # Substitui o ultimo elemento pela elite
        pop[n_pop-1] = elite

        g += 1
        
        arquivo.write(str(fit[idx]) + "\n")

    arquivo.close()

########################################################################################################

# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 4:
    print("Por favor, informe o tamanho da populacao, o numero de geracoes do arquivo como argumento e se deseja imprimir ou nao (1-sim 0-nao).")
    sys.exit()

# Copia os valores pras variaveis
n_pop = int(sys.argv[1])
n_ger = int(sys.argv[2])
grafico = int(sys.argv[3])

pop = []
pop = criaPopInicial(n_pop, pop)

# Chama o algoritmo genetico com o metoddo de cruzamento ab
genericAG(n_pop,pop,n_ger,1)
   
# Copia o conteudo pro arquivo ab
with open('saida_a.txt', 'r') as arquivo:
    conteudo = arquivo.read()

with open('saida_ab.txt', 'w') as arquivo:
    arquivo.write(conteudo)

# Chama o algoritmo genetico com o metoddo de cruzamento a
genericAG(n_pop,pop,n_ger,0)

if grafico == 1:
    plota(n_ger)