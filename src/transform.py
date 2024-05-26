# %%

import pandas as pd

import matplotlib.pyplot as plt
import os

from tqdm import tqdm

def process(path):

    with open(path, 'r') as open_file:
        data = open_file.readlines()

    rendimento_domiciliar = []
    rendimento_domiciliar_per_capita = []

    for line in data:

        value_1, value_2 = line[109:116], line[126:132]
        if value_1.strip(" ") == '' or value_2.strip(" ") == '':
            continue

        rendimento_domiciliar.append(int(value_1.replace(" ","0")))
        rendimento_domiciliar_per_capita.append(int(value_2.replace(" ","0")))

    return rendimento_domiciliar, rendimento_domiciliar_per_capita


all_files = []

for i in os.walk('../data/'):
    dirpath, dirnames, filenames = i
    filename = [i for i in filenames if "Domicilios" in i]
    if len(filename) > 0:
        filename = filename[-1]
        if filename.endswith(".txt"):
            all_files.append(f"{dirpath}/{filename}")

# %%

rendimento_domiciliar = []
rendimento_domiciliar_per_capita = []
for i in tqdm(all_files):
    data = process(i)
    rendimento_domiciliar.extend(data[0])
    rendimento_domiciliar_per_capita.extend(data[1])

df = pd.DataFrame({
    "rendimento_domiciliar": rendimento_domiciliar,
    "rendimento_domiciliar_per_capita": rendimento_domiciliar_per_capita
})

df.to_csv("../data/dados_rendimento.csv", index=False)
