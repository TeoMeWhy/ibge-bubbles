# %%

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

import seaborn as sns
sns.set_theme(style='darkgrid')

# %%

df = pd.read_csv('../data/dados_rendimento.csv')
df.head()

# %%

quantiles = np.arange(0.0025,1,0.0025).tolist() + [1]

percentiles = (df['rendimento_domiciliar_per_capita'].quantile(quantiles)
                                                     .reset_index()
                                                     .rename(columns={'index':'percentile',
                                                                      'rendimento_domiciliar_per_capita':'renda'})
               )

min_percentile = percentiles['renda'][percentiles['renda']>0].min()
percentiles['renda'] = percentiles['renda'].replace(0, min_percentile)

percentiles['x'] = list(range(1,21)) * 20
percentiles['y'] = pd.Series([[i] * 20 for i in range(1,21)]).explode().reset_index()[0]
percentiles['scale'] = percentiles['renda'] / percentiles['renda'].min()

def make_groups(x):
    if x <= 0.11:
        return "+ Pobres"

    elif x >= 0.99:
        return "+ Ricos"
    
    else:
        return "- Pobres"

percentiles['group_firts_11pct'] = percentiles['percentile'].apply(lambda x: '+ Pobres' if x <= 0.11  else '+ Ricos')
percentiles['group_firts_99pct'] = percentiles['percentile'].apply(lambda x: '+ Ricos' if x >= 0.99  else '+ Pobres')
percentiles['group_firts_11_99pct'] = percentiles['percentile'].apply(make_groups)

paleta = ['#000000', '#1a1aff', '#ff0066', '#e6e600']

# %%
# PLOT GERAL SEM GRUPOS
plt.figure(dpi=500)
sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    alpha=0.9,
    sizes=(1, 10000),
    legend=False,
    palette=paleta[0:1],
)

plt.suptitle('População Brasileira por 500k Habitantes')
plt.title('Somos todos iguais')
plt.xlabel('')
plt.ylabel('')
plt.savefig('pop_brasil_iguais.png')

# %%
# PLOT GERAL COM GRUPO DE MAIS POBRES

plt.figure(dpi=500)
sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    hue='group_firts_11pct',
    alpha=0.7,
    sizes=(1, 10000),
    legend=False,
    palette=paleta,
)
plt.suptitle('População Brasileira por 500k Habitantes')
plt.title('Somos todos iguais')
plt.xlabel('')
plt.ylabel('')
plt.savefig('pop_brasil_iguais_color_11.png')

# %%
# PLOT GERAL COM GRUPO DE MAIS RICOS

plt.figure(dpi=500)
sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    hue='group_firts_99pct',
    alpha=0.7,
    sizes=(1, 10000),
    legend=False,
    palette=paleta,
)

plt.suptitle('População Brasileira por 500k Habitantes')
plt.title('Somos todos iguais')
plt.xlabel('')
plt.ylabel('')
plt.savefig('pop_brasil_iguais_color_99.png')

# %%
# PLOT GERAL COM GRUPO DE MAIS POBRES E RICOS

plt.figure(dpi=500)
sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    hue='group_firts_11_99pct',
    alpha=0.7,
    sizes=(1, 10000),
    legend=False,
    palette=paleta,
)

plt.suptitle('População Brasileira por 500k Habitantes')
plt.title('Somos todos iguais')
plt.xlabel('')
plt.ylabel('')
plt.savefig('pop_brasil_iguais_color_11_99.png')

# %%

# PLOT GERAL RENDA

plt.figure(dpi=500)
scatter = sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    size='scale',
    alpha=0.7,
    sizes=(percentiles['scale'].min(), percentiles['scale'].max()),
    legend=False,
    palette=paleta,
)

plt.suptitle('População Brasileira a cada 500k')
plt.title('não tão iguais assim (maior a bola, maior a renda)')
plt.xlabel('')
plt.ylabel('')
plt.ylim([0,28])
plt.xlim([0,28])
plt.savefig('pop_brasil_nao_iguais.png')

# %%

# PLOT GERAL RENDA E GRUPOS

plt.figure(dpi=500)
scatter = sns.scatterplot(
    data=percentiles,
    x='x',
    y='y',
    size='scale',
    alpha=0.5,
    sizes=(percentiles['scale'].min(), percentiles['scale'].max()),
    legend=False,
    palette=paleta,
    hue='group_firts_11_99pct',
)

plt.suptitle('População Brasileira a cada 500k')
plt.title('não tão iguais assim (maior a bola, maior a renda)')
plt.xlabel('')
plt.ylabel('')
plt.ylim([0,28])
plt.xlim([0,28])
plt.savefig('pop_brasil_nao_iguais_color.png')

# %%
group_rend = percentiles.groupby(['group_firts_11_99pct'])['renda'].sum().astype(int)

group_rend / percentiles['renda'].sum()

# %%
group_rend['+ Ricos'] / group_rend['+ Pobres']
# %%
