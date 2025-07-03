import os
import pandas as pd
from dash import callback, Output, Input, State, clientside_callback

from components.figures import Figures
from components.processamento import DataProcessing

BASE_DIR = os.getcwd()
FILE_PATH_DATASET = os.path.join(BASE_DIR, 'components/datasets', 'RECLAMEAQUI_HAPVIDA.csv')    
df = pd.read_csv(FILE_PATH_DATASET, sep=',', encoding='utf-8')

# Mudança thema darck e white
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)

# Habilitar menu mobile
@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar

# Preencher label para seleção tamanho da palavra
@callback(Output("filtro-tamanho-texto-output", "children"), Input("filtro-tamanho-texto", "value"))
def update_value_slider(value):
    return f"Tamanho do texto selecionado: {value}"


# --- Atualizar todos os gráficos e a WordCloud ---
@callback(
    Output('grafico-serie-temporal', 'figure'),
    Output('grafico-freq-estado', 'figure'),
    Output('grafico-freq-status', 'figure'),
    Output('grafico-dist-texto', 'figure'),
    Output('mapa-brasil-heatmap', 'figure'),
    Output('grafico-wordcloud', 'src'),
    Input('filtro-estado', 'value'),
    Input('filtro-status', 'value'),
    Input('filtro-tamanho-texto', 'value'),
    Input('seletor-ano-mapa', 'value'),
    Input('color-scheme-toggle', 'theme'),
)
def atualizar_painel(estados_selec, status_selec, faixa_tamanho, ano_mapa, theme):
    dff = DataProcessing(df=df).data_texto()

    # --- Filtragem dos Dados ---    
    if estados_selec:
        dff = dff[dff['ESTADO'].isin(estados_selec)]
    if status_selec:
        dff = dff[dff['STATUS'].isin(status_selec)]

    dff = dff[(dff['TAMANHO_TEXTO'] >= faixa_tamanho[0]) & (dff['TAMANHO_TEXTO'] <= faixa_tamanho[1])]

    # --- Geração dos Gráficos ---
    # 1. Série Temporal

    fig_serie_temporal = Figures(df=dff).serie_temporal_data()

    # 2. Frequência por Estado

    fig_freq_estado = Figures(df=dff).freq_estado_data()

    # 3. Frequência por Status
    
    fig_freq_status = Figures(df=dff).freq_status_data()

    # 4. Distribuição do Tamanho do Texto
    
    fig_dist_texto = Figures(df=dff).freq_dist_texto()

    # 5. Mapa do Brasil

    fig_mapa = Figures(df=dff).map_data(ano_mapa=ano_mapa)

    # 6. WordCloud
    
    src_wordcloud = Figures(df=dff).freq_wordcloud()

    return fig_serie_temporal, fig_freq_estado, fig_freq_status, fig_dist_texto, fig_mapa, src_wordcloud
