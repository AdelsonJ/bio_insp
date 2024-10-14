import random
import math
import copy
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import sys

# Função para carregar as distâncias entre cidades de um arquivo
def carregar_dados_cidades():
    with open("instancia.txt", 'r') as arquivo:
        linhas = arquivo.readlines()
        numero_cidades = len(linhas)
        matriz = []

        for linha in linhas:
            dados_linha = list(map(float, linha.strip().split()))
            matriz.append(dados_linha)

    return numero_cidades, np.array(matriz)

# Calcula a inversa da distância total (fitness) de um caminho
def calcular_fitness(caminho, matriz_distancias):
    distancia_total = sum(matriz_distancias[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
    distancia_total += matriz_distancias[caminho[-1], caminho[0]]  # Retorno ao início
    return 1 / distancia_total

# Gera uma população inicial de soluções (anticorpos)
def criar_populacao(tamanho_pop, numero_cidades):
    return [np.random.permutation(numero_cidades) for _ in range(tamanho_pop)]

# Gera uma nova população adicionando soluções aleatórias
def expandir_populacao(populacao_atual, incremento, numero_cidades):
    nova_populacao = copy.deepcopy(populacao_atual)
    for _ in range(incremento):
        nova_populacao.append(np.random.permutation(numero_cidades))
    return nova_populacao

# Função de clonagem proporcional ao fitness
def realizar_clonagem(individuo, fitness, taxa_clonagem, tamanho_populacao):
    num_clones = int(round(taxa_clonagem * tamanho_populacao / (fitness + 1)))
    return [np.copy(individuo) for _ in range(num_clones)]

# Aplica uma mutação a um anticorpo, trocando dois elementos
def aplicar_mutacao(anticorpo, taxa_mutacao):
    if np.random.rand() < taxa_mutacao:
        i, j = np.random.choice(len(anticorpo), size=2, replace=False)
        anticorpo[i], anticorpo[j] = anticorpo[j], anticorpo[i]

# Função principal do algoritmo clonal
def algoritmo_clonal(matriz_distancias, tam_populacao, num_iteracoes):
    # Definindo parâmetros
    selecao_top = 10
    novas_solucoes = 5
    fator_clonagem = 2

    numero_cidades = len(matriz_distancias)
    populacao = criar_populacao(tam_populacao, numero_cidades)
    fitness_populacao = [calcular_fitness(anticorpo, matriz_distancias) for anticorpo in populacao]
    melhor_solucao = None
    melhor_distancia = float('inf')
    historico_melhores = []

    for geracao in range(num_iteracoes):
        # Seleção das melhores soluções
        indices_melhores = np.argsort(fitness_populacao)[-selecao_top:]
        melhores_solucoes = [populacao[i] for i in indices_melhores]
        melhores_fitness = [fitness_populacao[i] for i in indices_melhores]

        # Clonagem das melhores soluções
        clones = []
        for i in range(selecao_top):
            clones += realizar_clonagem(melhores_solucoes[i], melhores_fitness[i], fator_clonagem, tam_populacao)

        # Mutação nos clones gerados
        for clone in clones:
            fitness_clone = calcular_fitness(clone, matriz_distancias)
            aplicar_mutacao(clone, np.exp(-fitness_clone))

        # Avaliação dos clones mutados
        fitness_clones = [calcular_fitness(clone, matriz_distancias) for clone in clones]

        # Substituição da população
        indices_clones_melhores = np.argsort(fitness_clones)[-selecao_top:]
        populacao = [clones[i] for i in indices_clones_melhores]
        fitness_populacao = [fitness_clones[i] for i in indices_clones_melhores]

        # Expansão da população com soluções aleatórias
        populacao = expandir_populacao(populacao, novas_solucoes, numero_cidades)
        fitness_populacao = [calcular_fitness(anticorpo, matriz_distancias) for anticorpo in populacao]

        # Atualizando a melhor solução
        indice_melhor = np.argmax(fitness_populacao)
        melhor_caminho_atual = populacao[indice_melhor]
        distancia_atual = 1 / fitness_populacao[indice_melhor]

        if distancia_atual < melhor_distancia:
            melhor_solucao = melhor_caminho_atual
            melhor_distancia = distancia_atual

        historico_melhores.append(melhor_distancia)

    return melhor_solucao, historico_melhores

# Plotar gráfico da evolução da solução
def exibir_grafico_evolucao(iteracoes, historico_melhores):
    plt.plot(range(iteracoes), historico_melhores, linestyle='', marker='o', color='blue')
    plt.title('Melhor Caminho no Algoritmo Clonal')
    plt.xlabel('Iterações')
    plt.ylabel('Melhor Distância')
    plt.grid(True)
    plt.show()

# Configurações iniciais do algoritmo
tamanho_populacao = int(sys.argv[1])
numero_iteracoes = int(sys.argv[2])
exibir_grafico = int(sys.argv[3])

# Carregar dados da matriz de distâncias
numero_cidades, matriz_distancias = carregar_dados_cidades()

# Executar o algoritmo clonal
melhor_caminho, historico_melhores = algoritmo_clonal(matriz_distancias, tamanho_populacao, numero_iteracoes)

# Escrever os resultados em arquivos
with open('saida.txt', 'w') as arquivo:
    for valor in historico_melhores:
        arquivo.write(f"{valor}\n")

with open('saida_caminho.txt', 'w') as arquivo:
    for cidade in melhor_caminho:
        arquivo.write(f"{cidade}\n")
    arquivo.write(f"\nMelhor distância: {historico_melhores[-1]}\n")

# Exibir gráfico, se solicitado
if exibir_grafico:
    exibir_grafico_evolucao(numero_iteracoes, historico_melhores)
