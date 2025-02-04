import random
import math
import csv

def carregar_clientes_csv(caminho_arquivo):
    clientes = []
    with open(caminho_arquivo, newline='') as arquivo_csv:
        leitor = csv.reader(arquivo_csv, delimiter=';')
        next(leitor) 
        for linha in leitor:
            clientes.append((int(linha[1]), int(linha[2])))  
    return clientes

def calcular_distancia(posicao_cliente, posicao_ap):
    return math.sqrt((posicao_cliente[0] - posicao_ap[0])**2 + (posicao_cliente[1] - posicao_ap[1])**2)

def avaliacao(individuo, clientes, aps, capacidades):
    carga_aps = [0] * len(aps)
    distancia_total = 0

    for indice_cliente, indice_ap in enumerate(individuo):
        carga_aps[indice_ap] += 1
        distancia_total += calcular_distancia(clientes[indice_cliente], aps[indice_ap])

 
    penalidade_sobrecarga = sum(max(0, carga_aps[i] - capacidades[i])  for i in range(len(aps)))

    
    penalidade_balanceamento = sum((carga_aps[i] - sum(capacidades) / len(aps)) for i in range(len(aps)))

    
    distancia_normalizada = distancia_total / len(clientes)

    return distancia_normalizada + penalidade_sobrecarga + penalidade_balanceamento

def gerar_individuo(num_clientes, aps, clientes):
    individual = []
    for cliente_pos in clientes:
        closest_ap = min(range(len(aps)), key=lambda i: calcular_distancia(cliente_pos, aps[i]))
        individual.append(closest_ap)
    return individual


def cruzamento(pai1, pai2):
   
    ponto1 = random.randint(1, len(pai1) - 2)
    ponto2 = random.randint(ponto1, len(pai1) - 1)
    return pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]

def mutacao(individuo, num_aps, geracao, max_geracoes):
    
    taxa_mutacao = 0.1 * (1 - geracao / max_geracoes)
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = random.randint(0, num_aps - 1)

def selecao_torneio(populacao, valores_avaliacao, tamanho_torneio=8):
 
    selecionados = []
    for _ in range(len(populacao)):
        candidatos = random.sample(list(zip(populacao, valores_avaliacao)), tamanho_torneio)
        selecionados.append(min(candidatos, key=lambda x: x[1])[0])
    return selecionados
print()
def algoritmo_genetico(clientes, aps, capacidades, tamanho_populacao=100, geracoes=500):
    num_clientes = len(clientes)
    num_aps = len(aps)

  
    populacao = [gerar_individuo(num_clientes, aps, clientes) for _ in range(tamanho_populacao)]

    melhor_avaliacao = float('inf')
    contagem_sem_melhoria = 0

    for geracao in range(geracoes):
        valores_avaliacao = [avaliacao(ind, clientes, aps, capacidades) for ind in populacao]
        melhor_avaliacao_atual = min(valores_avaliacao)

        # Verifica se houve melhoria
        if melhor_avaliacao_atual < melhor_avaliacao:
            melhor_avaliacao = melhor_avaliacao_atual
            contagem_sem_melhoria = 0
        else:
            contagem_sem_melhoria += 1
        
        if contagem_sem_melhoria > 50:  
            break
        
        
        populacao = selecao_torneio(populacao, valores_avaliacao)

        
        while len(populacao) < tamanho_populacao:
            pai1 = random.choice(populacao[:10])  
            pai2 = random.choice(populacao[:10])
            filho = cruzamento(pai1, pai2)
            mutacao(filho, num_aps, geracao, geracoes) 
            populacao.append(filho)

        print(f"Geração {geracao+1}: Melhor Avaliação = {round(melhor_avaliacao, 2)}")

   
    melhor_individuo = min(populacao, key=lambda ind: avaliacao(ind, clientes, aps, capacidades))
    return [(i, melhor_individuo[i]) for i in range(len(melhor_individuo))]


if __name__ == "__main__":
    
    aps = [(0, 0), (80, 0), (0, 80), (80, 80)]
    capacidades = [64, 64, 128, 128]

    clientes = carregar_clientes_csv("posicoes.csv")

    
    melhor_solucao = algoritmo_genetico(clientes, aps, capacidades)
    print("\n-----Mapeamento de Clientes para APs-----\n")
    for cliente, ap in melhor_solucao:
        print(f"   Cliente {cliente+1} está conectado ao AP {ap+1}")
