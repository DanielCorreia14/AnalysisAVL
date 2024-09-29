import csv
import matplotlib.pyplot as plt
import random
from main import read_csv, BinarySearchTree, AVLTree, time_operations, time_search_operations

# Função para gerar gráficos de desempenho de inserção e busca
def plot_assintotic_analysis(data, subset_sizes):
    bst_insertion_times = []
    avl_insertion_times = []
    bst_heights = []
    avl_heights = []
    bst_search_times = []
    avl_search_times = []

    for size in subset_sizes:
        subset = random.sample(data, size)

        bst_time, bst_height = time_operations(BinarySearchTree, subset, 'Track')
        avl_time, avl_height = time_operations(AVLTree, subset, 'Track')
        bst_search_time = time_search_operations(BinarySearchTree, subset, 'Track')
        avl_search_time = time_search_operations(AVLTree, subset, 'Track')

        bst_insertion_times.append(bst_time)
        avl_insertion_times.append(avl_time)
        bst_heights.append(bst_height)
        avl_heights.append(avl_height)
        bst_search_times.append(bst_search_time)
        avl_search_times.append(avl_search_time)

    # Gráfico de desempenho de inserção
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    plt.plot(subset_sizes, bst_insertion_times, label='BST - Tempo de Inserção', marker='o')
    plt.plot(subset_sizes, avl_insertion_times, label='AVL - Tempo de Inserção', marker='o')
    plt.xlabel('Tamanho do Conjunto de Dados')
    plt.ylabel('Tempo de Inserção (segundos)')
    plt.title('Desempenho de Inserção')
    plt.legend()
    plt.grid(True)

    # Gráfico de busca
    plt.subplot(1, 2, 2)
    plt.plot(subset_sizes, bst_search_times, label='BST - Tempo de Busca', marker='o')
    plt.plot(subset_sizes, avl_search_times, label='AVL - Tempo de Busca', marker='o')
    plt.xlabel('Tamanho do Conjunto de Dados')
    plt.ylabel('Tempo de Busca (segundos)')
    plt.title('Desempenho de Busca')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_assintotica.png')
    plt.show()

# Leitura dos dados
data = read_csv('ClassicHit.csv')
subset_sizes = [1000, 5000, 10000]

# Gerar gráficos de análise assintótica
plot_assintotic_analysis(data, subset_sizes)
