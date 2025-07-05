import os
import pandas as pd

import plotly.express as px
from dash import callback, Output, Input, State, clientside_callback

from components.processamento import DataProcessing, GeoJsonSingleton

BASE_DIR = os.getcwd()
FILE_PATH_DATASET = os.path.join(BASE_DIR, 'components/datasets', 'RECLAMEAQUI_HAPVIDA.csv')    
df = pd.read_csv(FILE_PATH_DATASET, sep=',', encoding='utf-8')

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
)
def atualizar_painel(estados_selec, status_selec, faixa_tamanho, ano_mapa):
    dff_ = DataProcessing(df=df)

    dff = dff_.data_texto()

    # --- Filtragem dos Dados ---    
    if estados_selec:
        dff = dff[dff['ESTADO'].isin(estados_selec)]
    if status_selec:
        dff = dff[dff['STATUS'].isin(status_selec)]

    dff = dff[(dff['TAMANHO_TEXTO'] >= faixa_tamanho[0]) & (dff['TAMANHO_TEXTO'] <= faixa_tamanho[1])]

    # --- Geração dos Gráficos ---
    # 1. Série Temporal

    fig_serie_temporal = px.line(
            dff_.series_temporal(),
            x='MES', 
            y='CONTAGEM',
            title='Série Temporal de Reclamações', 
            labels={'MES': 'Mês', 'CONTAGEM': 'Nº Reclamações'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 2. Frequência por Estado

    fig_freq_estado = px.bar(
            dff_.data_estado(), 
            x='ESTADO', 
            y='count', 
            title='Reclamações por Estado', 
            labels={'ESTADO': 'Estado', 'count': 'Nº Reclamações'}, 
            text_auto=True
        ).update_xaxes(categoryorder="total descending").update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 3. Frequência por Status
    
    fig_freq_status = px.pie(
            dff_.data_status(),
            names='STATUS', 
            values='count', 
            title='Distribuição por Status', 
            hole=0.4
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 4. Distribuição do Tamanho do Texto
    
    fig_dist_texto = px.histogram(
            dff_.data_texto(), 
            x='TAMANHO_TEXTO',             
            title='Distribuição do Tamanho do Texto',
            labels={'TAMANHO_TEXTO': 'Tamanho do Texto', 'count': 'Frequência'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 5. Mapa do Brasil    
       
    fig_mapa = px.choropleth_mapbox(
            dff_.data_mapa(ano_mapa=ano_mapa),
            geojson=GeoJsonSingleton(), 
            locations='ESTADO',             
            color='CONTAGEM', 
            color_continuous_scale="reds",
            mapbox_style="carto-positron", 
            zoom=3.2, 
            center={"lat": -14.2350, "lon": -51.9253},
            title=f'Reclamações em {ano_mapa}', 
            labels={'CONTAGEM': 'Nº Reclamações'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))

    # 6. WordCloud
    
    src_wordcloud = dff_.data_wordcloud()

    return fig_serie_temporal, fig_freq_estado, fig_freq_status, fig_dist_texto, fig_mapa, src_wordcloud
