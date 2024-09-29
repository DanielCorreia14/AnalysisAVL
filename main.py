import csv
import matplotlib.pyplot as plt
import time
import random
import pandas as pd

# Definindo a classe Node para a árvore
class Node:
    def __init__(self, key, data):
        self.left = None
        self.right = None
        self.key = key
        self.data = data

# Implementação da Árvore Binária de Busca (BST)
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert(self.root, key, data)

    def _insert(self, current_node, key, data):
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = Node(key, data)
            else:
                self._insert(current_node.left, key, data)
        else:
            if current_node.right is None:
                current_node.right = Node(key, data)
            else:
                self._insert(current_node.right, key, data)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, current_node, key):
        if current_node is None:
            return None
        if key == current_node.key:
            return current_node.data
        elif key < current_node.key:
            return self._search(current_node.left, key)
        else:
            return self._search(current_node.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return max(left_height, right_height) + 1

    def inorder_traversal(self):
        elements = []
        self._inorder_traversal(self.root, elements)
        return elements

    def _inorder_traversal(self, node, elements):
        if node:
            self._inorder_traversal(node.left, elements)
            elements.append((node.key, node.data))
            self._inorder_traversal(node.right, elements)

# Implementação da Árvore AVL
class AVLNode(Node):
    def __init__(self, key, data):
        super().__init__(key, data)
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return AVLNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        y = z.right
        if y is None:
            return z
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        if y is None:
            return z
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def inorder_traversal(self):
        elements = []
        self._inorder_traversal(self.root, elements)
        return elements

    def _inorder_traversal(self, node, elements):
        if node:
            self._inorder_traversal(node.left, elements)
            elements.append((node.key, node.data))
            self._inorder_traversal(node.right, elements)

# Função para ler o CSV e converter para uma lista de dicionários
def read_csv(file_name):
    with open(file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return data

# Função para medir o tempo de inserção e altura da árvore
def time_operations(TreeClass, data_list, key_attribute):
    tree = TreeClass()
    start_time = time.time()
    for item in data_list:
        if key_attribute in item:
            key = item[key_attribute]
            tree.insert(key, item)
    end_time = time.time()
    insertion_time = end_time - start_time
    height = tree.height()
    return insertion_time, height

# Função para medir o tempo de busca
def time_search_operations(TreeClass, data_list, key_attribute):
    tree = TreeClass()
    for item in data_list:
        if key_attribute in item:
            key = item[key_attribute]
            tree.insert(key, item)
    
    search_times = []
    keys_to_search = [random.choice(data_list).get(key_attribute) for _ in range(100)]
    for key in keys_to_search:
        if key is not None:
            start_time = time.time()
            tree.search(key)
            end_time = time.time()
            search_times.append(end_time - start_time)
    return sum(search_times) / len(search_times) if search_times else 0

# Função para criar gráficos de desempenho
def plot_performance(subset_sizes, bst_times, avl_times, bst_heights, avl_heights, search_bst_times, search_avl_times, title):
    plt.figure(figsize=(14, 7))

    plt.subplot(2, 2, 1)
    plt.plot(subset_sizes, bst_times, label='BST - Tempo de Inserção', marker='o')
    plt.plot(subset_sizes, avl_times, label='AVL - Tempo de Inserção', marker='o')
    plt.xlabel('Tamanho do Conjunto de Dados')
    plt.ylabel('Tempo de Inserção (segundos)')
    plt.title('Desempenho de Inserção')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(subset_sizes, bst_heights, label='BST - Altura', marker='o')
    plt.plot(subset_sizes, avl_heights, label='AVL - Altura', marker='o')
    plt.xlabel('Tamanho do Conjunto de Dados')
    plt.ylabel('Altura da Árvore')
    plt.title('Altura da Árvore')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(subset_sizes, search_bst_times, label='BST - Tempo de Busca', marker='o')
    plt.plot(subset_sizes, search_avl_times, label='AVL - Tempo de Busca', marker='o')
    plt.xlabel('Tamanho do Conjunto de Dados')
    plt.ylabel('Tempo de Busca (segundos)')
    plt.title('Desempenho de Busca')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f'{title}.png')

# Função para plotar o gráfico de músicas lançadas a cada 3 anos
def plot_songs_by_year(data):
    df = pd.DataFrame(data)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    df['Year Group'] = (df['Year'] // 3) * 3  # Agrupando a cada 3 anos
    songs_by_year = df.groupby('Year Group').size()

    plt.figure(figsize=(10, 6))
    songs_by_year.plot(kind='bar', color='skyblue')
    plt.title('Número de Músicas Lançadas a Cada 3 Anos')
    plt.xlabel('Ano (Agrupado a Cada 3 Anos)')
    plt.ylabel('Número de Músicas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('songs_by_year.png')

# Função para gerar um relatório em TXT
def generate_performance_report(bst_results, avl_results, file_name):
    with open(file_name, 'w') as f:
        f.write("Relatório de Desempenho - Árvore Binária de Busca (BST) vs Árvore AVL\n")
        f.write("=====================================================================\n\n")
        
        f.write("Comparação de Tempo de Inserção:\n")
        for size in bst_results['sizes']:
            f.write(f"Tamanho do Conjunto de Dados: {size} - BST: {bst_results['insert_times'][size]:.6f} seg, AVL: {avl_results['insert_times'][size]:.6f} seg\n")
        
        f.write("\nComparação de Altura das Árvores:\n")
        for size in bst_results['sizes']:
            f.write(f"Tamanho do Conjunto de Dados: {size} - BST: {bst_results['heights'][size]}, AVL: {avl_results['heights'][size]}\n")
        
        f.write("\nComparação de Tempo de Busca:\n")
        for size in bst_results['sizes']:
            f.write(f"Tamanho do Conjunto de Dados: {size} - BST: {bst_results['search_times'][size]:.6f} seg, AVL: {avl_results['search_times'][size]:.6f} seg\n")

# Função principal
def main():
    file_name = 'ClassicHit.csv'
    data = read_csv(file_name)
    
    bst_insert_times = {}
    avl_insert_times = {}
    bst_heights = {}
    avl_heights = {}
    bst_search_times = {}
    avl_search_times = {}
    subset_sizes = [1000, 5000, 10000]

    for size in subset_sizes:
        subset_data = data[:size]

        bst_time, bst_height = time_operations(BinarySearchTree, subset_data, 'Track')
        avl_time, avl_height = time_operations(AVLTree, subset_data, 'Track')

        bst_insert_times[size] = bst_time
        avl_insert_times[size] = avl_time
        bst_heights[size] = bst_height
        avl_heights[size] = avl_height

        bst_search_time = time_search_operations(BinarySearchTree, subset_data, 'Track')
        avl_search_time = time_search_operations(AVLTree, subset_data, 'Track')

        bst_search_times[size] = bst_search_time
        avl_search_times[size] = avl_search_time

    # Prepare data for report
    bst_results = {
        'sizes': subset_sizes,
        'insert_times': bst_insert_times,
        'heights': bst_heights,
        'search_times': bst_search_times
    }
    
    avl_results = {
        'sizes': subset_sizes,
        'insert_times': avl_insert_times,
        'heights': avl_heights,
        'search_times': avl_search_times
    }

    plot_performance(subset_sizes, list(bst_insert_times.values()), list(avl_insert_times.values()), list(bst_heights.values()), list(avl_heights.values()), list(bst_search_times.values()), list(avl_search_times.values()), 'performance')

    generate_performance_report(bst_results, avl_results, 'performance_report.txt')

    plot_songs_by_year(data)

if __name__ == '__main__':
    main()
