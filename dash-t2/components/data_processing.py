# data_processing.py

import os
import pandas as pd
import geopandas as gpd
import unidecode

# Define a pasta base (diretório onde está este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos
FILE_PATH_DATASET = os.path.join(BASE_DIR, 'datasets', 'RECLAMEAQUI_HAPVIDA.csv')
FILE_PATH_SHP = os.path.join(BASE_DIR, 'datasets', 'BR_Municipios_2024', 'BR_Municipios_2024.shp')

# O arquivo final será o mesmo tratado
FILE_PATH_OUTPUT = os.path.join(BASE_DIR, 'datasets', 'RECLAMEAQUI_HAPVIDA_treat.csv')

def load_data(file_path):
    #Carrega o dataset original.
    
    df = pd.read_csv(file_path, sep=',', encoding='utf-8')
    return df

def split_city_state(df, column='LOCAL'):
    # Divide a coluna "LOCAL" no formato 'Cidade - UF' em duas colunas separadas: 'Cidade' e 'UF'.
    
    if column in df.columns:
        split_cols = df[column].str.split(' - ', expand=True)
        df['Cidade'] = split_cols[0]
        df['UF'] = split_cols[1]
        df.drop(columns=[column], inplace=True)
    return df

def padronizar_nome(texto):
    #Padroniza nomes removendo acentos e deixando em maiúsculo.
    
    return unidecode.unidecode(str(texto)).strip().upper()

def main():
    # 1) Leitura do CSV original
    print(f"Lendo arquivo: {FILE_PATH_DATASET}")
    df = load_data(FILE_PATH_DATASET)
    print(f"Dataset carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.")

    # 2) Separar Cidade e UF
    df = split_city_state(df, column='LOCAL')

    # 3) Preparar dados para merge
    df['Cidade_merge'] = df['Cidade'].apply(padronizar_nome)
    df['UF_merge'] = df['UF'].apply(lambda x: str(x).upper())

    # 4) Carregar shapefile e padronizar
    print(f"Lendo shapefile: {FILE_PATH_SHP}")
    gdf = gpd.read_file(FILE_PATH_SHP)
    print("Colunas encontradas no shapefile:", gdf.columns.tolist())

    # Substitua NM_MUN e SIGLA_UF pelos nomes reais das colunas do seu shapefile
    gdf['Cidade_merge'] = gdf['NM_MUN'].apply(padronizar_nome)
    gdf['UF_merge'] = gdf['SIGLA_UF'].apply(lambda x: str(x).upper())

    # 5) Merge
    merged_df = df.merge(
        gdf[['Cidade_merge', 'UF_merge', 'geometry']],
        on=['Cidade_merge', 'UF_merge'],
        how='left',
        indicator=True
    )
    print(f"Merge realizado. Registros combinados: {merged_df['_merge'].value_counts().to_dict()}")

    # 6) Limpar colunas de controle e salvar tudo no mesmo arquivo treat
    merged_df.drop(columns=['Cidade_merge', 'UF_merge', '_merge']).to_csv(FILE_PATH_OUTPUT, index=False, sep=',')
    print(f"Arquivo tratado e mesclado salvo como {FILE_PATH_OUTPUT}")