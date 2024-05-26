# %%

import pandas as pd
import requests 

import zipfile
import os

from tqdm import tqdm

# %%

ufs = [
    'AC','AL','AP','AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA','MT','MS','MG',
    'PA','PB','PR','PE','PI',
    'RJ','RN','RS','RO','RR',
    'SC','SP1','SP2_RM','SE',
    'TO',
 ]

url = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados/{uf}.zip"

def download_url(url, save_path):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=256):
            fd.write(chunk)

print("realizando download...")

for i in tqdm(ufs):
    download_url(url.format(uf=i), f"../data/{i}.zip")

files = [i for i in os.listdir("../data/") if i.endswith(".zip")]
print("extraindo...")
for i in tqdm(files):
    with zipfile.ZipFile(f"../data/{i}","r") as zip_ref:
        folder = f"../data/"
        zip_ref.extractall(folder)

