from collections import deque
import concurrent.futures
import time

grafo = {
    "RH": ["Financeiro", "TI"],
    "Financeiro": ["RH", "Marketing"],
    "TI": ["RH", "Operações"],
    "Marketing": ["Financeiro", "Vendas"],
    "Vendas": ["Marketing"],
    "Operações": ["TI"]
}

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
                if vizinho not in caminho:
                    fila.append(caminho + [vizinho])

    return caminhos

def busca_paralela(entrada):
    grafo, (inicio, destino) = entrada
    return ((inicio, destino), busca_largura_todos_caminhos(grafo, inicio, destino))

def principal():
    nos = list(grafo.keys())
    pares_de_nos = [(a, b) for i, a in enumerate(nos) for b in nos[i+1:] if a != b]

    

    tempo_inicio_seq = time.time()
    resultados_sequencial = [busca_paralela((grafo, par)) for par in pares_de_nos]
    tempo_fim_seq = time.time()
    tempo_total_seq = tempo_fim_seq - tempo_inicio_seq
    print(resultados_sequencial)
    print(f"\nTempo de execução SEQUENCIAL: {tempo_total_seq:.6f} segundos")

    tempo_inicio_par = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        resultados_paralelo = list(executor.map(busca_paralela, [(grafo, par) for par in pares_de_nos]))
    tempo_fim_par = time.time()
    tempo_total_par = tempo_fim_par - tempo_inicio_par
    print(resultados_paralelo)
    print(f"Tempo de execução PARALELA: {tempo_total_par:.6f} segundos")

    ganho = tempo_total_seq / tempo_total_par if tempo_total_par > 0 else float('inf')
    print(f"\nGanho de desempenho com paralelismo: {ganho:.6f}x mais rápido")



if __name__ == "__main__":
    principal()
