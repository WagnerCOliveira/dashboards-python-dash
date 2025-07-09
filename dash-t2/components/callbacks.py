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
    return f"Selecione os valores entre: {value}"

# --- Atualizar o gráfico de mappa ---
@callback(
    Output('mapa-brasil-heatmap', 'figure'),
    Input('seletor-ano-mapa', 'value'),    
)
def atualizar_mapa(ano_mapa):
    # Instanciando CLasse processamento dados.
    dff_ = DataProcessing(df=df)      

    # 5. Mapa do Brasil
    #map_data = dff[dff['ANO'] == ano_mapa].groupby('ESTADO').size().reset_index(name='CONTAGEM')
    fig_mapa = px.choropleth_mapbox(
        dff_.data_mapa(ano_mapa=ano_mapa),
        geojson=GeoJsonSingleton(), 
        locations='ESTADO',         
        color='CONTAGEM', 
        color_continuous_scale="reds",
        mapbox_style="carto-positron", 
        zoom=2.5, 
        center={"lat": -14.2350, "lon": -51.9253},
        title=f'Reclamações em {ano_mapa}', labels={'CONTAGEM': 'Nº Reclamações'}
    ).update_layout(title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))

    if ano_mapa is None:
        return fig_mapa

    return fig_mapa

# --- Atualizar todos os gráficos e a WordCloud ---
@callback(
    Output('grafico-serie-temporal', 'figure'),
    Output('grafico-freq-estado', 'figure'),
    Output('grafico-freq-status', 'figure'),
    Output('grafico-dist-texto', 'figure'),    
    Output('grafico-wordcloud', 'src'),
    Input('filtro-estado', 'value'),
    Input('filtro-status', 'value'),
    Input('filtro-tamanho-texto', 'value'),
    
)
def atualizar_painel(estados_selec, status_selec, faixa_tamanho):
    # Instanciando CLasse processamento dados.
    dff_ = DataProcessing(df=df)
    # Copia DF original
    dff = dff_.data_texto()    

    # --- Filtragem dos Dados ---    
    if estados_selec:
        dff = dff[dff['ESTADO'].isin(estados_selec)]
    if status_selec:
        dff = dff[dff['STATUS'].isin(status_selec)]

    dff = dff[(dff['TAMANHO_TEXTO'] >= faixa_tamanho[0]) & (dff['TAMANHO_TEXTO'] <= faixa_tamanho[1])]

    # --- Geração dos Gráficos ---

    # 1. Série Temporal
    serie_temporal_data = dff.groupby('MES').size().reset_index(name='CONTAGEM')
    fig_serie_temporal = px.line(
        serie_temporal_data, 
        x='MES', 
        y='CONTAGEM',         
        title='Série Temporal de Reclamações', 
        labels={'MES': 'Mês', 'CONTAGEM': 'Nº Reclamações'}
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 2. Frequência por Estado
    freq_estado_data = dff['ESTADO'].value_counts().reset_index()
    fig_freq_estado = px.bar(
        freq_estado_data, x='ESTADO', 
        y='count',         
        title='Reclamações por Estado', labels={'ESTADO': 'Estado', 'count': 'Nº Reclamações'}, 
        text_auto=True
    ).update_xaxes(categoryorder="total descending").update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 3. Frequência por Status
    freq_status_data = dff['STATUS'].value_counts().reset_index()
    fig_freq_status = px.pie(
        freq_status_data, 
        names='STATUS', 
        values='count',         
        title='Distribuição por Status', hole=0.4
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 4. Distribuição do Tamanho do Texto
    fig_dist_texto = px.histogram(
        dff, x='TAMANHO_TEXTO',         
        title='Distribuição do Tamanho do Texto',
        labels={'TAMANHO_TEXTO': 'Tamanho do Texto', 'count': 'Frequência'}
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))
                              

    # 6. WordCloud
       
    src_wordcloud = dff_.data_wordcloud()

    return fig_serie_temporal, fig_freq_estado, fig_freq_status, fig_dist_texto, src_wordcloud
