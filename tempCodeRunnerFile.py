from collections import deque
import concurrent.futures
import time

# ----------------------------
# 1. Construção do Grafo
# ----------------------------
grafo = {
    "RH": ["Financeiro", "TI"],
    "Financeiro": ["RH", "Marketing"],
    "TI": ["RH", "Operações"],
    "Marketing": ["Financeiro", "Vendas"],
    "Vendas": ["Marketing"],
    "Operações": ["TI"]
}

# ----------------------------------------------------------------
# 2. Implementação da BFS para encontrar todos os caminhos
# ----------------------------------------------------------------
def busca_largura_todos_caminhos(grafo, inicio, destino):
    fila = deque([[inicio]])
    caminhos = []

    while fila:
        caminho = fila.popleft()
        no_atual = caminho[-1]

        if no_atual == destino:
            caminhos.append(caminho)
        else:
            for vizinho in grafo.get(no_atual, []):
                if vizinho not in caminho:  # evita ciclos
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    fila.append(novo_caminho)

    return caminhos

# ----------------------------------------------------------------------
# 3. Função paralela para aplicar a busca entre dois nós do grafo
# ----------------------------------------------------------------------
def busca_paralela(entrada):
    grafo, (inicio, destino) = entrada
    return ((inicio, destino), busca_largura_todos_caminhos(grafo, inicio, destino))

# ----------------------------------------------
# 4. Execução principal com comparação de tempos
# ----------------------------------------------
def principal():
    # Gerar todos os pares possíveis de nós diferentes
    nos = list(grafo.keys())
    pares_de_nos = [(a, b) for i, a in enumerate(nos) for b in nos[i+1:] if a != b]

    # --------------------
    # Execução sequencial
    # --------------------
    print("\nExecutando busca sequencial...")
    tempo_inicio = time.time()
    resultados_sequencial = [busca_paralela((grafo, par)) for par in pares_de_nos]
    tempo_fim = time.time()
    print(f"Tempo (sequencial): {tempo_fim - tempo_inicio:.4f} segundos")

    # --------------------
    # Execução paralela
    # --------------------
    print("\nExecutando busca paralela com ProcessPoolExecutor...")
    tempo_inicio = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        resultados_paralelo = list(executor.map(busca_paralela, [(grafo, par) for par in pares_de_nos]))
    tempo_fim = time.time()
    print(f"Tempo (paralelo): {tempo_fim - tempo_inicio:.4f} segundos")

    # --------------------
    # Mostrar alguns resultados
    # --------------------
    print("\nExemplo de caminhos encontrados:")
    for (inicio, destino), caminhos in resultados_paralelo:
        print(f"\nCaminhos de {inicio} para {destino}:")
        for caminho in caminhos:
            print(" -> ".join(caminho))

# ----------------------
# Execução do programa
# ----------------------
if __name__ == "__main__":
    principal()
