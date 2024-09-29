import csv
import matplotlib.pyplot as plt
import pandas as pd

def read_csv(file_path):
    return pd.read_csv(file_path)

# função para analise de dados
def analyze_data(df):
    output = []

    # distribuição de generos
    genre_distribution = df['Genre'].value_counts()
    output.append("Distribuição de Gêneros:\n")
    output.append(genre_distribution.to_string())
    
    # analise temporal com agrupamento de 3 em 3 anos
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year_Group'] = (df['Year'] // 3) * 3  # Agrupando os anos em intervalos de 3 anos
    year_distribution = df['Year_Group'].value_counts().sort_index()

    # gráfico de Colunas
    plt.figure(figsize=(10, 6))
    plt.bar(year_distribution.index, year_distribution.values, width=2, color='skyblue', alpha=0.6)
    plt.title('Quantidade de Músicas Lançadas Agrupadas por 3 Anos')
    plt.xlabel('Anos (Agrupados)')
    plt.ylabel('Quantidade de Músicas')
    plt.xticks(year_distribution.index, rotation=45)

    plt.tight_layout()
    plt.savefig('analise_temporal_colunas.png')
    plt.close()

    output.append("\nAnálise Temporal: Gráfico salvo como 'analise_temporal_colunas.png'.")

    # Análise de Popularidade
    avg_popularity = df['Popularity'].mean()
    output.append(f"\nMédia de Popularidade: {avg_popularity:.2f}")

    correlation = df[['Energy', 'Danceability', 'Popularity']].corr()
    output.append("\nCorrelação entre Atributos:\n")
    output.append(correlation.to_string())

    # agrupamento por Artista
    artist_group = df.groupby('Artist').agg({'Track': 'count', 'Popularity': 'max'}).reset_index()
    artist_group.columns = ['Artista', 'Quantidade de Músicas', 'Música Mais Popular']
    output.append("\nAgrupamento por Artista:\n")
    output.append(artist_group.to_string(index=False))

    with open('analise_saida.txt', 'w') as f:
        f.write('\n'.join(output))
    print("Análise concluída e salva em 'analise_saida.txt'.")


file_path = 'ClassicHit.csv'


if __name__ == "__main__":
    df = read_csv(file_path)
    analyze_data(df)
