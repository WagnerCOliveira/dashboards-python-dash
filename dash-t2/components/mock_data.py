import pandas as pd
import numpy as np


def gerar_dados_aleatorios(num_registros=2000):
    """Gera um DataFrame com dados de reclamações fictícias."""
    np.random.seed(42)
    estados = ['SP', 'RJ', 'MG', 'RS', 'BA', 'PR', 'SC', 'CE', 'GO', 'DF']
    status_opcoes = ['Não Resolvido', 'Resolvido', 'Em Réplica']
    textos_base = [
        "produto com defeito na entrega", "cobrança indevida na fatura", "atendimento ao cliente péssimo",
        "demora para resolver meu problema", "cancelamento de serviço não efetuado", "propaganda enganosa",
        "dificuldade para troca de produto", "suporte técnico não responde", "problemas com o estorno do valor",
        "qualidade do material muito baixa"
    ]

    data = {
        'DATA': pd.to_datetime(pd.date_range(start='2022-01-01', end='2025-06-28', periods=num_registros)),
        'ESTADO': np.random.choice(estados, num_registros, p=[0.25, 0.20, 0.15, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]),
        'STATUS': np.random.choice(status_opcoes, num_registros, p=[0.4, 0.5, 0.1]),
        'DESCRICAO': [f"{np.random.choice(textos_base)} - ID {i}" for i in range(num_registros)]
    }
    df = pd.DataFrame(data)
    df['TAMANHO_TEXTO'] = df['DESCRICAO'].str.len()
    df['ANO'] = df['DATA'].dt.year
    df['MES'] = df['DATA'].dt.to_period('M').astype(str)
    return df