import pandas as pd

df = pd.read_csv("./components/dataset/berkeley_preprocessado.csv")

def genero():

    frequencia_genero = pd.DataFrame(
        df['GENERO'].value_counts()
    ).rename(columns={'count': 'COUNT'})

    total_genero = frequencia_genero.sum()

    frequencia_genero['DISTRIBUICAO'] = (
        frequencia_genero / total_genero * 100
    ).round(2)

    frequencia_genero = frequencia_genero.reset_index()

    return frequencia_genero


def representatividade_m_f_admis_depar():

    df_aceitacao = pd.DataFrame(
        df.groupby(['DEPARTAMENTO', 'GENERO', 'ADMISSAO'], as_index=False)
        .size()
    ).rename(columns={'size': 'COUNT'})

    return df_aceitacao