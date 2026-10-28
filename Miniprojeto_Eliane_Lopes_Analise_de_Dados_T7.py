"""
Mini-Projeto Avaliativo - Módulo 1
Aluna: Eliane Lopes  |  Turma: Analise_de_Dados_T7
Análise Exploratória de Dados (AED) - Base Varejo

Como rodar: coloque este arquivo e o 'Base Varejo.csv' na mesma pasta e execute
    python Miniprojeto_Eliane_Lopes_Analise_de_Dados_T7.py
"""

import re
import pandas as pd

print("==========================================================")
print(" SPRINT 1: Importação dos dados ")
print("==========================================================")

# 1. Carregando a base de dados
# Usando sep=';' porque o arquivo veio com ponto e vírgula
df = pd.read_csv('Base Varejo.csv', sep=';', encoding='utf-8')

# Como o CSV termina cada linha com ';;;;', o pandas criou colunas vazias sem nome.
# Vou apagar essas colunas porque não têm nenhuma informação.
colunas_vazias = [c for c in df.columns if c.startswith('Unnamed')]
df = df.drop(columns=colunas_vazias)

# Pegando a quantidade de linhas e colunas
quantidade_linhas = df.shape[0]
quantidade_colunas = df.shape[1]

print("Número de registros (linhas):", quantidade_linhas)
print("Número de colunas:", quantidade_colunas)

print("\nTipos de dados originais:")
print(df.dtypes)

print("\nPrimeiras linhas:")
print(df.head())


print("\n==========================================================")
print(" SPRINT 2 e 3: Limpeza de Dados ")
print("==========================================================")

# ----- Verificando os problemas ANTES de limpar -----
print("Valores vazios (nulos) encontrados:")
print(df.isnull().sum())

# A base usa o texto '#N/D' (erro do Excel) no lugar de vazio, então o isnull()
# não encontra. Vou contar esse "nulo escondido" separadamente.
nd_categoria = (df['PR_CAT'] == '#N/D').sum()
nd_nome = (df['PR_NOME'] == '#N/D').sum()
print("\nNulos escondidos como '#N/D' em PR_CAT:", nd_categoria)
print("Nulos escondidos como '#N/D' em PR_NOME:", nd_nome)

duplicadas = df.duplicated().sum()
print("\nLinhas duplicadas encontradas:", duplicadas)

datas_teste = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
print("Datas inválidas encontradas:", datas_teste.isnull().sum())


# ----- Funções de limpeza (Sprint 2) -----
def limpar_texto(texto):
    """Tira espaços das pontas, espaços duplos e deixa em maiúsculo (usa regex)."""
    texto = str(texto).strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto.upper()


def limpar_inteiro(valor):
    """Tira tudo que não é número (regex) e devolve inteiro. Se não der, devolve None."""
    so_numeros = re.sub(r'[^\d]', '', str(valor))
    if so_numeros == '':
        return None
    return int(so_numeros)


# 2. Limpando os textos
for coluna in ['CL_GENERO', 'CL_SEG', 'PR_CAT', 'PR_NOME']:
    df[coluna] = df[coluna].apply(limpar_texto)

# 3. Limpando os números inteiros (ids, estado civil e filhos)
for coluna in ['CO_ID', 'CL_ID', 'CL_EC', 'CL_FHL', 'PR_ID']:
    df[coluna] = df[coluna].apply(limpar_inteiro)

# 4. Tratando a coluna de data
# Convertendo o texto para o formato de data (datetime) do pandas
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
print("\n-> Pronto! Coluna de data convertida para datetime.")
print("Período da base:", df['DATA'].min().strftime('%d/%m/%Y'), "até", df['DATA'].max().strftime('%d/%m/%Y'))

# Se alguma data não tiver sido convertida, a linha é removida, porque sem data
# não dá para analisar o tempo e não existe um valor correto para colocar no lugar.
antes = len(df)
df = df.dropna(subset=['DATA'])
print("Linhas removidas por data inválida:", antes - len(df))


# 5. Tratando os nulos
# Categoria vazia (ou '#N/D') vira 'Sem Categoria'.
# Escolhi NÃO apagar essas linhas porque o produto foi vendido: apagar mudaria
# as contagens de compras e itens. E não dá para descobrir a categoria certa.
def preencher_categoria(categoria):
    if categoria == '#N/D' or categoria == '' or categoria == 'NAN':
        return 'Sem Categoria'
    else:
        return categoria


df['PR_CAT'] = df['PR_CAT'].apply(preencher_categoria)
print("-> Pronto! Categorias vazias ou '#N/D' viraram 'Sem Categoria':", nd_categoria)

# O nome do produto '#N/D' também é um nulo escondido (é o mesmo produto sem categoria)
df['PR_NOME'] = df['PR_NOME'].replace('#N/D', 'PRODUTO NAO IDENTIFICADO')

# Colunas numéricas (estado civil e filhos): se tivesse nulo, eu preencheria com a
# mediana, porque ela não é puxada por valores extremos. Nesta base não tem nenhum.
for coluna in ['CL_EC', 'CL_FHL']:
    nulos = df[coluna].isnull().sum()
    if nulos > 0:
        df[coluna] = df[coluna].fillna(df[coluna].median())
    print("Nulos em", coluna, ":", nulos)

# A base não tem dimensões físicas do produto (peso, altura...), então não há o que tratar.
print("Dimensões físicas: não existem nesta base.")

# Os ids não podem ser preenchidos, então se faltar algum a linha é removida
df = df.dropna(subset=['CO_ID', 'CL_ID', 'PR_ID'])
df['CO_ID'] = df['CO_ID'].astype(int)
df['CL_ID'] = df['CL_ID'].astype(int)
df['PR_ID'] = df['PR_ID'].astype(int)
df['CL_EC'] = df['CL_EC'].astype(int)
df['CL_FHL'] = df['CL_FHL'].astype(int)


# 6. Tratando as duplicatas
# A base não tem coluna de quantidade. Então uma linha repetida na mesma compra
# significa que o cliente levou o mesmo produto mais de uma vez.
# Se eu apagasse com drop_duplicates(), eu perderia venda de verdade.
# Por isso junto as linhas repetidas em uma só e guardo quantas eram na coluna QTD.
colunas = list(df.columns)
df = df.groupby(colunas).size().reset_index(name='QTD')
print("\n-> Pronto! Duplicatas juntadas em uma linha só (coluna QTD).")
print("Linhas agora:", len(df), "| Unidades vendidas (soma de QTD):", df['QTD'].sum())


# 7. Validando a regra do número da compra (CO_ID)
# Uma compra tem vários itens, mas todos devem ser do MESMO cliente e da MESMA data.
verifica = df.groupby('CO_ID').agg(clientes=('CL_ID', 'nunique'), datas=('DATA', 'nunique'))
compras_erradas = verifica[(verifica['clientes'] > 1) | (verifica['datas'] > 1)].index

# As compras com problema são separadas em outra tabela e saem da análise
df_inconsistentes = df[df['CO_ID'].isin(compras_erradas)]
df = df[~df['CO_ID'].isin(compras_erradas)]

print("\nCompras distintas na base:", verifica.shape[0])
print("Compras com mais de um cliente ou mais de uma data:", len(compras_erradas))
print("Registros separados como inconsistentes:", len(df_inconsistentes))

print("\nBase final:", df.shape[0], "linhas e", df.shape[1], "colunas")
print("Nulos restantes:", df.isnull().sum().sum())


print("\n==========================================================")
print(" SPRINT 4: Estatísticas Descritivas (Número de filhos) ")
print("==========================================================")

# O número de filhos é uma característica do CLIENTE, mas a tabela tem uma linha
# por item comprado. Se eu calculasse direto, quem compra mais pesaria mais na média.
# Por isso fico com uma linha por cliente antes de calcular.
clientes = df.drop_duplicates('CL_ID')
filhos = clientes['CL_FHL']

# Calculando estatística por estatística separadamente
contagem = filhos.count()
media = filhos.mean()
mediana = filhos.median()
desvio = filhos.std()
moda = filhos.mode()[0]
maximo = filhos.max()
minimo = filhos.min()
quartil_25 = filhos.quantile(0.25)
quartil_50 = filhos.quantile(0.50)
quartil_75 = filhos.quantile(0.75)

# Mostrando os resultados na tela (usando round para arredondar a média e o desvio)
print("Contagem (clientes):", contagem)
print("Média:", round(media, 2))
print("Mediana:", mediana)
print("Moda:", moda)
print("Desvio Padrão:", round(desvio, 2))
print("Mínimo:", minimo, "| Máximo:", maximo)
print("Quartis -> 25%:", quartil_25, "| 50%:", quartil_50, "| 75%:", quartil_75)

print("\nClientes por número de filhos:")
print(filhos.value_counts().sort_index())
percentual_sem_filhos = round((filhos == 0).sum() / contagem * 100, 1)
print("Clientes sem filhos:", percentual_sem_filhos, "%")


print("\n==========================================================")
print(" SPRINT 5: Padrões de Agrupamento ")
print("==========================================================")

total_itens = df['QTD'].sum()

# Agrupamento 1: Qual gênero tem mais vendas e mais compras?
print("\n1. Itens vendidos e compras por Gênero:")
agrupamento_genero = df.groupby('CL_GENERO').agg(itens=('QTD', 'sum'), compras=('CO_ID', 'nunique'), clientes=('CL_ID', 'nunique'))
print(agrupamento_genero)

# Média de itens por compra de cada gênero
itens_por_compra = df.groupby(['CL_GENERO', 'CO_ID'])['QTD'].sum().groupby('CL_GENERO').mean().round(1)
print("\nMédia de itens por compra:")
print(itens_por_compra)

# Agrupamento 2: Quais são as categorias que mais vendem?
print("\n2. Itens vendidos por Categoria:")
agrupamento_categoria = df.groupby('PR_CAT').agg(itens=('QTD', 'sum'), compras=('CO_ID', 'nunique'))
agrupamento_categoria['percentual'] = (agrupamento_categoria['itens'] / total_itens * 100).round(1)
# Ordenando para o maior aparecer primeiro
agrupamento_categoria = agrupamento_categoria.sort_values('itens', ascending=False)
print(agrupamento_categoria)

# Agrupamento 3: Segmento do cliente
print("\n3. Itens vendidos por Segmento do cliente:")
agrupamento_segmento = df.groupby('CL_SEG').agg(itens=('QTD', 'sum'), compras=('CO_ID', 'nunique'), clientes=('CL_ID', 'nunique'))
agrupamento_segmento['percentual'] = (agrupamento_segmento['itens'] / total_itens * 100).round(1)
agrupamento_segmento = agrupamento_segmento.sort_values('itens', ascending=False)
print(agrupamento_segmento)

# Agrupamento 4: cruzando categoria com gênero (pivot_table)
print("\n4. Itens por Categoria x Gênero (pivot_table):")
tabela_cruzada = pd.pivot_table(df, index='PR_CAT', columns='CL_GENERO', values='QTD', aggfunc='sum', fill_value=0)
print(tabela_cruzada)

# Agrupamento 5: vendas por ano
print("\n5. Itens e compras por Ano:")
df['ANO'] = df['DATA'].dt.year
agrupamento_ano = df.groupby('ANO').agg(itens=('QTD', 'sum'), compras=('CO_ID', 'nunique'))
print(agrupamento_ano)

# Quantos dias de venda existem em cada mês? (importante para interpretar o tempo)
df['MES'] = df['DATA'].dt.to_period('M')
por_mes = df.groupby('MES').agg(itens=('QTD', 'sum'), dias=('DATA', 'nunique'))
print("\nDias com venda por mês: mínimo", por_mes['dias'].min(), "| máximo", por_mes['dias'].max())
print("Total de dias com venda na base:", df['DATA'].nunique())


print("\n==========================================================")
print(" CONCLUSÕES ")
print("==========================================================")

genero_top = agrupamento_genero['itens'].idxmax()
categoria_top = agrupamento_categoria.index[0]
segmento_top = agrupamento_segmento.index[0]

print("1. A base tinha", quantidade_linhas, "linhas. Depois da limpeza ficaram", len(df),
      "linhas com", total_itens, "itens vendidos em", df['CO_ID'].nunique(),
      "compras de", df['CL_ID'].nunique(), "clientes.")
print("2. O gênero", genero_top, "tem mais itens e mais compras, mas a diferença é pequena:",
      "a média de itens por compra é quase igual entre F e M.")
print("3. A categoria que mais vende é", categoria_top, "com",
      agrupamento_categoria['percentual'].iloc[0], "% dos itens.")
print("4. Número de filhos por cliente: média", round(media, 2), "| mediana", mediana,
      "| moda", moda, "->", percentual_sem_filhos, "% dos clientes não têm filhos.")
print("5. O segmento", segmento_top, "concentra", agrupamento_segmento['percentual'].iloc[0],
      "% dos itens vendidos.")
print("6. Problemas que continuam: a base não tem valor em R$ nem quantidade (QTD foi",
      "calculada pelas linhas repetidas), há", nd_categoria, "itens sem categoria e",
      "poucos dias de venda por mês, então não dá para falar de sazonalidade.")


print("\n==========================================================")
print(" SPRINT 6: Exportar Base Limpa ")
print("==========================================================")

# Salvando a tabela final limpa (sem as colunas auxiliares de ano e mês)
df = df.drop(columns=['ANO', 'MES'])
df.to_csv('df_limpo.csv', index=False, sep=';', encoding='utf-8')
print("Sucesso! Arquivo 'df_limpo.csv' foi salvo na pasta.")