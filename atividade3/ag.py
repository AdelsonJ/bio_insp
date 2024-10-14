import random
import copy
import matplotlib.pyplot as plt
import sys


# Funcao que cria a populacao inicial
def criaPopInicial(npop, pop, ncrom):
    for i in range(npop):
        aux = []
        for j in range(ncrom):
            aux.append(random.randint(0,1))
        pop.append(aux)

    return pop

# Descobre o fitness da funcao
def avaliaPop(npop, pop, ncrom, peso, valor, capacidade, tipo):
    fit = []

    for i in range (npop):
        # Faz um somatorio que calcula o peso e os valores totais de cada elemento
        somatorio_pesos = 0
        somatorio_valores = 0
        for j in range (ncrom):
            if pop[i][j] == 1:
                somatorio_pesos += peso[j]
                somatorio_valores += valor[j]

        if somatorio_pesos <= capacidade:
            fit.append(somatorio_valores)
        else:
            if tipo == 0:
                fit.append(somatorio_valores * (1-(somatorio_pesos - capacidade)/capacidade))
            else:
                fit.append(somatorio_valores - (somatorio_valores * (somatorio_pesos - capacidade)))
    
    return fit

# Seleciona os pais da proxima geracao pelo método do torneio
def torneio(npop, fit):
    pais = [0] * npop

    pv = 0.9
    i = 0

    while i < npop:
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
            vencedor = menor
        else: 
            vencedor = maior
        
        pais[i] = vencedor
        i += 1

    return pais

# Seleciona os pais da proxima geracao pelo método da roleta
def roleta(npop, fit):
    pais = []
    soma = sum(fit)
    
    # Se a soma das aptidões for zero, selecionar aleatoriamente
    if soma == 0:
        pais = list(range(npop))
    else:
        roleta = [f/soma for f in fit]
        while len(pais) < npop:
            r = random.uniform(0, 1)
            percorre = 0
            for i, p in enumerate(roleta):
                percorre += p
                if r <= percorre:
                    pais.append(i)
                    break
    return pais


# Funcao que faz  o cruzamento entre os pais
def cruzamento(npop, pais, pop, ncrom, tx_cruz):
    filho_1 = []
    filho_2 = []
    pop_inter = []

    for i in range(0, npop-1, 2):
        #Confere se os elementos serão cruzados ou não
        m  = random.uniform(0,1)
        if m <= tx_cruz:
            # Sorteia um numero para poder ser o tanto de
            # informacao que sera combinada entre os pais 
            r = random.randint(1, ncrom)
            j = 0

            # Faz a troca de informacao
            while j < r:
                filho_1.append(pop[pais[i+1]][j])
                filho_2.append(pop[pais[i]][j])
                j+= 1
            
            # Conserva a informacao do outro pai
            while j < ncrom:
                filho_1.append(pop[pais[i]][j])
                filho_2.append(pop[pais[i+1]][j])
                j+= 1

            pop_inter.append(filho_1)
            pop_inter.append(filho_2)
        else:
            pop_inter.append(pop[pais[i]])
            pop_inter.append(pop[pais[i+1]])

    return pop_inter


# Funcao que faz a mutacao para cada alelo do gene
def mutacao(npop, pop, ncrom, tx_mut):
    for i in range(npop):
        for j in range (ncrom):
            r = random.randint(0, 100)
            r = r/100
            if r <= tx_mut:
                if pop[i][j] == 0:
                    pop[i][j] = 1
                else:
                    pop[i][j] = 0
    return pop
    
# Funcao que seleciona o melhor elemento daquela populacao
def elitismo(npop, fit):
    maior = -float('inf') 
    idx = 0

    for i in range(npop):
        if fit[i] > maior:
            maior = fit[i]
            idx = i

    return idx

# Funcao que imprime a populacao
def imprimePop(npop, pop, ncrom):
    for i in range(npop):
        for j in range(ncrom):
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
    plt.plot(geracoes, resultados_1, label = "Torneio",  linestyle='', marker='o', color='blue')
    plt.plot(geracoes, resultados_2, label = "Roleta",  linestyle='', marker='*', color='red')
    plt.title('Algoritmo Genético')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor resultado')
    plt.grid(True)
    plt.legend()
    plt.show()      

# Funcao principal que comanda o algortimo genetico
def genericAG(npop, nger, ncrom, peso, valor, capacidade, tipo, pop, tipo_2):
    arquivo =  open("saida_1.txt","w")
    
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
        fit = avaliaPop(npop, pop, ncrom, peso, valor, capacidade, tipo_2)

        # Cria o vetor de pais
        if tipo == 0:
            pais = torneio(npop, fit)
        else:
            pais = roleta(npop, fit)

        #Cruza a população de pais e faz a mutação
        pop_inter = cruzamento(npop, pais, pop, ncrom, tx_cruz)
        pop_inter = mutacao(npop, pop_inter, ncrom, tx_mut)

        # Recebe o index do elemento de melhor fitness
        idx = elitismo(npop, fit)
        elite = pop[idx] 

        # Copia a populacao intermediaria pra principal
        pop = copy.deepcopy(pop_inter)

        # Substitui o ultimo elemento pela elite
        pop[npop-1] = elite

        g += 1
        
        melhor_elem.append(fit[idx])
        
    for elemento in melhor_elem:
        arquivo.write(str(elemento) + "\n")
        
    arquivo.close()
    
    if tipo == 0:
        arquivo_2 = open("saida_2.txt", "r")
        conteudo = list(map(int, arquivo_2))
        melhor = conteudo[-1]
        arquivo_2.close()
    else:
        melhor = 0

    # Compara com o resultado obtido anteriormente (se esse existir) 
    # Se ele for menor que a elite do novo resultado, então substui no arquivo resposta
    if fit[idx] < melhor:
        arquivo =  open("p_s.txt","w")
        for j in range (ncrom):
            arquivo.write(str(pop[idx][j]) + "\n")
            
        arquivo.close()

###############################################################################################################################################################

# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 5:
    print("Por favor, informe o tamanho da populacao, o numero de geracoes do arquivo como argumento, o tipo de penalização (0 para branda e 1 para severa) e se deseja imprimir ou nao (1-sim 0-nao).")
    sys.exit()

# Copia os valores pras variaveis
npop = int(sys.argv[1])
nger = int(sys.argv[2])
tipo_2 = int(sys.argv[3])
grafico = int(sys.argv[4])

with open('p_c.txt', 'r') as arquivo:
    capacidade = int(arquivo.read())

with open('p_w.txt', 'r') as arquivo:
    pesos_str = arquivo.read().split()
    peso = list(map(int, pesos_str)) 

with open('p_p.txt', 'r') as arquivo:
    valor_str = arquivo.read().split()
    valor = list(map(int, valor_str)) 

ncrom = len(peso)

pop = []
criaPopInicial(npop, pop, ncrom)

# Chama a funcao do algoritmo genetico
genericAG(npop, nger, ncrom, peso, valor, capacidade, 1, pop, tipo_2)

with open('saida_1.txt', 'r') as arquivo:
    conteudo = arquivo.read()

with open('saida_2.txt', 'w') as arquivo:
    arquivo.write(conteudo)

# Chama a funcao do algoritmo genetico
genericAG(npop, nger, ncrom, peso, valor, capacidade, 1, pop, tipo_2)
    
if grafico == 1:
    plota()

arquivo.close()

