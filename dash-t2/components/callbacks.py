import io
import base64
import plotly.express as px
import plotly.io as pio
from dash import callback, Output, Input, State, clientside_callback
from wordcloud import WordCloud

from components.mock_data import gerar_dados_aleatorios

df = gerar_dados_aleatorios()

geojson_brasil_url = "https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/estado/geojson/estado.json"

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
    
    # --- Filtragem dos Dados ---
    dff = df.copy()
    if estados_selec:
        dff = dff[dff['ESTADO'].isin(estados_selec)]
    if status_selec:
        dff = dff[dff['STATUS'].isin(status_selec)]
    dff = dff[(dff['TAMANHO_TEXTO'] >= faixa_tamanho[0]) & (dff['TAMANHO_TEXTO'] <= faixa_tamanho[1])]

    # --- Geração dos Gráficos ---
    # 1. Série Temporal
    serie_temporal_data = dff.groupby('MES').size().reset_index(name='CONTAGEM')
    fig_serie_temporal = px.line(
        serie_temporal_data, x='MES', y='CONTAGEM',
        title='Série Temporal de Reclamações', labels={'MES': 'Mês', 'CONTAGEM': 'Nº Reclamações'}
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 2. Frequência por Estado
    freq_estado_data = dff['ESTADO'].value_counts().reset_index()
    fig_freq_estado = px.bar(
        freq_estado_data, x='ESTADO', y='count', 
        title='Reclamações por Estado', labels={'ESTADO': 'Estado', 'count': 'Nº Reclamações'}, text_auto=True
    ).update_xaxes(categoryorder="total descending").update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 3. Frequência por Status
    freq_status_data = dff['STATUS'].value_counts().reset_index()
    fig_freq_status = px.pie(
        freq_status_data, names='STATUS', values='count', 
        title='Distribuição por Status', hole=0.4
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 4. Distribuição do Tamanho do Texto
    fig_dist_texto = px.histogram(
        dff, x='TAMANHO_TEXTO', 
        title='Distribuição do Tamanho do Texto',
        labels={'TAMANHO_TEXTO': 'Tamanho do Texto', 'count': 'Frequência'}
    ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))

    # 5. Mapa do Brasil
    map_data = dff[dff['ANO'] == ano_mapa].groupby('ESTADO').size().reset_index(name='CONTAGEM')
    fig_mapa = px.choropleth_mapbox(
        map_data, geojson=geojson_brasil_url, locations='ESTADO', featureidkey="properties.sigla",
        color='CONTAGEM', color_continuous_scale="reds",
        mapbox_style="carto-positron", zoom=3.2, center={"lat": -14.2350, "lon": -51.9253},
        title=f'Reclamações em {ano_mapa}', labels={'CONTAGEM': 'Nº Reclamações'}
    )
    fig_mapa.update_layout(title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))

    # 6. WordCloud
    texto_completo = " ".join(dff['DESCRICAO'].dropna())
    # Garante que a nuvem não quebre se não houver texto
    if not texto_completo.strip():
        texto_completo = "Nenhuma palavra encontrada"
        
    wordcloud = WordCloud(
        width=400, 
        height=300,         
    ).generate(texto_completo)
    
    img_io = io.BytesIO()
    wordcloud.to_image().save(img_io, 'PNG')
    src_wordcloud = 'data:image/png;base64,{}'.format(base64.b64encode(img_io.getvalue()).decode())

    return fig_serie_temporal, fig_freq_estado, fig_freq_status, fig_dist_texto, fig_mapa, src_wordcloud
