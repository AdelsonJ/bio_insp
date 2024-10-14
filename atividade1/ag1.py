import random
import math
import copy
import matplotlib.pyplot as plt
import sys


# Funcao que cria a populacao inicial
def criaPopInicial(npop, pop):
    for i in range(npop):
        for j in range(18):
            pop[i][j] = random.randint(0, 1)
    return pop

# Funcao que transforma um dado numero binario em inteiro
def transfBinario(pop, posicao, inicial, final):
    inteiro = 0
    i = 0

    # Pega da posicao mais significativa ate a menos significativa
    for idx in range(final-1, inicial-1, -1):
        if pop[posicao][idx] == 1:
            inteiro += 2 ** i
        i += 1
 
    return -2 + (2-(-2))/((2**6)-1) * inteiro
        
# Discretiza o numero para que ele fique no range de [2,-2]        
def discretiza(pop, posicao):
    discretizado = [0] * 3

    # Separa os 18 bits iniciais em 3 grupos de 6 bits
    discretizado[0] = transfBinario(pop, posicao, 0, 6)
    discretizado[1] = transfBinario(pop, posicao, 6, 12)
    discretizado[2] = transfBinario(pop, posicao, 12, 18)

    return discretizado


# Descobre o fitness da funcao
def avaliaPop(npop, pop):

    fit = [0] * npop
    discretizado = [0] * 3

    for i in range (npop):
        discretizado = discretiza(pop,i)

        somatorio_1 = discretizado[0]**2 + discretizado[1]**2 + discretizado[2]**2

        somatorio_2 = math.cos(2* math.pi * discretizado[0]) + math.cos(2* math.pi * discretizado[1]) + math.cos(2* math.pi * discretizado[2])

        elevado_1 = 1/3 * somatorio_2

        elevado_2 = -0.2*(math.sqrt(1/3 * somatorio_1)) 

        fit[i]= -20*math.exp(elevado_2) - math.exp(elevado_1) + 20 + math.exp(1)
    
    return fit

# Seleciona os pais da proxima geracao
def torneio(npop, fit):
    v_pais = [0] * npop

    pv = 0.9
    i = 0

    while i < npop:
        # Seleciona aleatoriamente 4 numeros
        p1 = random.randint(0, npop-1)
        p2 = random.randint(0, npop-1)
        p3 = random.randint(0, npop-1)
        p4 = random.randint(0, npop-1)
        
        # Se um desse numeros for igual, seleciona outro
        while p1 == p2 or p2 == p3 or  p2 == p4:
            p2 = random.randint(0, npop-1)

        while p1 == p3 or p2 == p3 or p3 == p4:
            p3 = random.randint(0, npop-1)

        while p1 == p4 or p2 == p4 or p3 == p4:
            p4 = random.randint(0, npop-1)

        r = random.random()

        # Seleciona os maiores e menores elementos a partir do fitness de cada um
        if fit[p1] < fit[p2] and fit[p1] < fit[p3] and fit[p1] < fit[p4]:
            menor = p1
            maior = [p2,p3,p4]
        else:
            if fit[p2] < fit[p3] and fit[p2] < fit[p4]:
                menor = p2
                maior = [p1,p3,p4]
            else:
                if fit[p3] < fit[p4]:
                    menor = p3
                    maior = [p1,p2,p4]
                else:
                    menor = p4
                    maior = [p1,p2,p3]

        # Se o numero aleatorio r for maior que a probabilidade de vitoria,  
        # entao sorteia um novo numero que representara o novo vencedor.
        if r > pv:
            aux = random.randint(0,2)
            if aux == 0:
                vencedor = maior[0]
            elif aux == 2:
                vencedor = maior[1]
            else:
                vencedor = maior[2]
        else: 
            vencedor = menor
        
        v_pais[i] = vencedor
        i += 1

    return v_pais


# Funcao que faz  o cruzamento entre os pais
def cruzamento(npop, pais, pop):
    pop_inter = [[0]*18 for _ in range(npop)]

    for i in range(0, npop-1, 2):
        # Sorteia um numero para poder ser o tanto de
        # informacao que sera combinada entre os pais 
        r = random.randint(1, 18)
        j = 0

        # Faz a troca de informacao
        while j < r:
            pop_inter[i][j] = pop[pais[i+1]][j]
            pop_inter[i+1][j] = pop[pais[i]][j]
            j+= 1
        
        # Conserva a informacao do outro pai
        while j < 18:
            pop_inter[i][j] = pop[pais[i]][j]
            pop_inter[i+1][j] = pop[pais[i+1]][j]
            j+= 1

    return pop_inter


# Funcao que faz a mutacao para cada alelo do gene
def mutacao(npop, pop):
    for i in range(npop):
        for j in range (18):
            r = random.randint(0, 100)
            r = r/100
            if r <= 0.1:
                if pop[i][j] == 0:
                    pop[i][j] = 1
                else:
                    pop[i][j] = 0
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
        for j in range(18):
            print(str(pop[i][j]) + " ", end="")
        print() 
    pass


# Funcao principal que comanda o algortimo genetico
def genericAG(n_pop, n_ger):
    arquivo =  open("saida.txt","w")
    
    # Inicia as variaveis
    pop = [[0]*18 for _ in range(n_pop)]
    pop_inter = [[0]*18 for _ in range(n_pop)]
    pais = [0] * n_pop
    fit = [0] * n_pop


    criaPopInicial(n_pop, pop)
    g = 0

    # Faz o processo para cada geracao
    while g < n_ger:
        fit = avaliaPop(n_pop, pop)
        pais = torneio(n_pop, fit)
        pop_inter = cruzamento(n_pop, pais, pop)
        pop_inter = mutacao(n_pop, pop_inter)

        # Recebe o index do elemento de melhor fitness
        idx = elitismo(n_pop, fit)
        elite = pop[idx] 

        # Copia a populacao intermediaria pra principal
        pop = copy.deepcopy(pop_inter)

        # Substitui o ultimo elemento pela elite
        pop[n_pop-1] = elite

        g += 1
        
        arquivo.write(str(fit[idx]) + "\n")

    arquivo.close()


# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 3:
    print("Por favor, informe o tamanho da poupulacao e o numero de geracoes do arquivo como argumento.")
    sys.exit()

# Copia os valores pras variaveis
n_pop = int(sys.argv[1])
n_ger = int(sys.argv[2])

# Chama a funcao do algoritmo genetico
genericAG(n_pop,n_ger)
    
# Pega os resultados do arquivo e guarda numa variavel
with open('saida.txt', 'r') as arquivo:
    linhas = arquivo.readlines()

resultados = [float(linha.strip()) for linha in linhas]

geracoes = list(range(n_ger))

# Plota o grafico
plt.plot(geracoes, resultados)
plt.title('Algoritmo Genético')
plt.xlabel('Gerações')
plt.ylabel('Melhor resultado')
plt.grid(True)
plt.show()
