import dash_mantine_components as dmc
from dash import dcc, Input, Output, State, callback, clientside_callback, Patch, ALL
import plotly.express as px
import plotly.io as pio

from components.processamento import representatividade_m_f_admis_depar

dmc.add_figure_templates(default="mantine_dark")

df_aceitacao = representatividade_m_f_admis_depar()

df_grouped = df_aceitacao.groupby(["DEPARTAMENTO", "GENERO"])["COUNT"].sum().unstack(fill_value=0)
df_grouped["TOTAL"] = df_grouped.sum(axis=1)
df_grouped["PROPORCAO_F"] = (df_grouped["F"] / df_grouped["TOTAL"] * 100).round(2)
df_grouped["PROPORCAO_M"] = (df_grouped["M"] / df_grouped["TOTAL"] * 100).round(2)
df_grouped.reset_index()

scatter_fig = px.scatter(
    df_grouped.reset_index(),
    x="TOTAL",
    y="PROPORCAO_F",
    size="PROPORCAO_F",
    color="DEPARTAMENTO",
    log_x=True,
    size_max=60,
    title=f"Proporção de Departamento e Gênero",
)

bar_fig = px.histogram(
    representatividade_m_f_admis_depar(), 
    x="DEPARTAMENTO", 
    y="COUNT",       
    color='GENERO',
    barmode='group'
)

def make_graph_card(fig, index):
    return dmc.GridCol(
        dmc.Card(dcc.Graph(figure=fig, id={"index": index}), withBorder=True),
        span={"base": 12, "md": 6}
    )

graphs = dcc.Loading(dmc.Grid(
    [
        make_graph_card(bar_fig, "bar"),
        make_graph_card(scatter_fig, "scatter"),        
    ],
    gutter="xl",
    style={"height": 800}
),delay_hide=1000 )

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


@callback(
    Output({"index": ALL}, "figure"),
    Input("color-scheme-toggle", "checked"),
    State({"index": ALL}, "id"),
)
def update_figure(switch_on, ids):
    # template must be template object rather than just the template string name
    template = pio.templates["mantine_dark"] if switch_on else pio.templates["mantine_light"]
    patched_figures = []
    for i in ids:
        patched_fig = Patch()
        patched_fig["layout"]["template"] = template
        patched_figures.append(patched_fig)

    return patched_figures

layout = dmc.Container([     
    graphs
], fluid=True)
