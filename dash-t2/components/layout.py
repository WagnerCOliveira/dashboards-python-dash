import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc
from dash_iconify import DashIconify

from components import pie, data

# ==============================================================================
# 1. GERAÇÃO DE DADOS ALEATÓRIOS (MOCK DATA)
# ==============================================================================

from components import mock_data

df = mock_data.gerar_dados_aleatorios()

logo = "https://unifor.br/o/unifor-theme/images/unifor-logo-horizontal-negative.svg"

theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]),
    onLabel=DashIconify(icon="radix-icons:moon", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][6]),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)


about = dcc.Markdown("""
    Trabalho para disciplina Introdução a python - Ciencia de Dados.

    Projeto de T2 - O Conjunto de Dados de Admissões de Pós-Graduação de Berkeley em 1973.

    - Levanta questões centrais sobre a equidade nos processos seletivos em instituições de ensino superior. 
    Os dados, à primeira vista, indicam uma desigualdade de gênero nas admissões, sugerindo que mulheres tinham 
    menor probabilidade de serem aceitas em comparação aos homens. Essa evidência inicial gerou um debate sobre 
    a possibilidade de discriminação institucional contra mulheres no ambiente acadêmico

    Atividade

    - Desenvolver uma análise exploratória de dados que identifique padrões e propondo interpretações sobre viés 
    e desigualdade na admissão de pós-graduação da Universidade de Berkeley em 1973.
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
                                dmc.Image(src=logo, h=50),
                                dmc.Title("Projeto de T2", c="blue"),
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
                                theme_toggle
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
                p="md",  # Padding geral do Navbar
                children=[
                    # Use dmc.Stack para agrupar e espaçar verticalmente os seus componentes
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
                                id='seletor-ano',    
                                clearable=True,                             
                                data=[{'label': str(ano), 'value': str(ano)} for ano in sorted((df['ANO'].unique()))],                                
                            ),
                            dmc.Slider(                                
                                id='filtro-tamanho-texto', 
                                min=df['TAMANHO_TEXTO'].min(), 
                                max=df['TAMANHO_TEXTO'].max(),
                                value=[df['TAMANHO_TEXTO'].min(), df['TAMANHO_TEXTO'].max()],                                
                            ),
                        ],
                        gap="xl"
                    )
                ],
            ),
            dmc.AppShellMain(
                children= [                 
                    #pie.StatsRing(),
                    dmc.MantineProvider(data.layout)                    
                ]
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

    return dmc.MantineProvider(layout)