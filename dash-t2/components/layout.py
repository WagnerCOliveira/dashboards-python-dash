import os
import dash_mantine_components as dmc
import pandas as pd

from dash import dcc, html
from dash_iconify import DashIconify

from components.processamento import DataProcessing

BASE_DIR = os.getcwd()
FILE_PATH_DATASET = os.path.join(BASE_DIR, 'components/datasets', 'RECLAMEAQUI_HAPVIDA.csv')    
df = DataProcessing(df=pd.read_csv(FILE_PATH_DATASET, sep=',', encoding='utf-8')).data_texto()

about = dcc.Markdown("""
    PROJETO – DASHBOARD COM DADOS DO RECLAME AQUI
    ---
                     
    ### MBA em Ciência de Dados – Disciplina: Dashboards em Python
    
    Prof. Túlio Ribeiro
    
    ### Descrição    

    Painel interativo com **Dash** utilizando dados de reclamações do Reclame Aqui.
    do **Hapvida**.
    
    """, style={"width": 450})

def body():

    layout = dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Group(
                            [
                                dmc.Burger(
                                    id="burger",
                                    size="sm",
                                    hiddenFrom="sm",
                                    opened=False,
                                ),                                
                                dmc.Title("Dashboard - Reclame Aqui", c="blue"),
                            ]
                        ),
                        dmc.Group(
                            [
                                dmc.HoverCard(
                                    shadow="lg",
                                    children=[
                                        dmc.HoverCardTarget(dmc.Button("About",variant="outline")),
                                        dmc.HoverCardDropdown(about),
                                    ],
                                ),
                               
                            ]
                        ),
                        
                    ], 
                    justify="space-between",
                    h="100%",
                    px="md",
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                p="md",
                children=[                    
                    dmc.Stack(
                        children=[
                            dmc.MultiSelect(
                                label='Filtrando Estado',
                                placeholder="Filtrar por Estado...",
                                id='filtro-estado',                                 
                                data=[{'label': i, 'value': i} for i in sorted(df['ESTADO'].unique())],                                
                            ),
                            dmc.MultiSelect(
                                label='Filtrando Status',
                                id='filtro-status', 
                                placeholder="Filtrar por Status...",
                                data=[{'label': i, 'value': i} for i in df['STATUS'].unique()],                                
                            ),
                            dmc.Select(
                                label='Selecionando po Ano',
                                placeholder="Filtrar por Ano (mapa)...",
                                id='seletor-ano-mapa',    
                                clearable=True,                             
                                data=[{'label': str(ano), 'value': str(ano)} for ano in sorted((df['ANO'].unique()))],                                
                            ),
                            dmc.Text(id='filtro-tamanho-texto-output'),
                            dmc.RangeSlider(                                
                                restrictToMarks=False,                                
                                id='filtro-tamanho-texto', 
                                min=df['TAMANHO_TEXTO'].min(), 
                                max=df['TAMANHO_TEXTO'].max(),
                                value=[df['TAMANHO_TEXTO'].min(), df['TAMANHO_TEXTO'].max()],
                                marks=[
                                    {'value': df['TAMANHO_TEXTO'].min(), 'label': df['TAMANHO_TEXTO'].min(), },
                                    {'value': df['TAMANHO_TEXTO'].max(), 'label': df['TAMANHO_TEXTO'].max(), }
                                ]                                
                            ),
                        ],
                        gap="xl"
                    )
                ],
            ),
            dmc.AppShellMain(    
                dmc.Grid(
                    align="stretch",
                    justify="space-around",                                 
                    children=[
                        dcc.Loading(
                            dmc.Grid([
                                dmc.GridCol(
                                    dmc.Card(
                                        dcc.Graph(id='grafico-dist-texto'),                                                                
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                                dmc.GridCol(
                                    dmc.Card(
                                        dcc.Graph(id='grafico-serie-temporal'),                                
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                                dmc.GridCol(
                                    dmc.Card(
                                        dcc.Graph(id='grafico-freq-status'),                                 
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                                dmc.GridCol(
                                    dmc.Card(                                
                                        html.Img(id='grafico-wordcloud', className="img-fluid w-100"),                                 
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                                dmc.GridCol(
                                    dmc.Card(
                                        id='mapa-brasil-heatmap',
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                                dmc.GridCol(
                                    dmc.Card(
                                        dcc.Graph(id='grafico-freq-estado' ),                                 
                                    ), span={"base": 12, "md": 6, "lg": 6}),
                            ],
                            gutter="md",
                            
                            )
                        ),                                                
                    ] 
                )        
            ),
        ],
        header={
            "height": {"base": 60, "md": 70, "lg": 80},
        },
        navbar={
            "width": {"base": 200, "md": 300, "lg": 400},
            "breakpoint": "sm",
            "collapsed": {"mobile": True},
        },
        padding="md",
        id="appshell",
    )

    return layout