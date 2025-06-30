import pandas as pd
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from .callbacks import genero

df = pd.DataFrame(genero())

stats_masculino = df.loc[(df['GENERO'] == 'M')]['COUNT'].values
progress_masculino = df.loc[(df['GENERO'] == 'M')]['DISTRIBUICAO'].values

stats_feminino = df.loc[(df['GENERO'] == 'F')]['COUNT'].values
progress_feminino = df.loc[(df['GENERO'] == 'F')]['DISTRIBUICAO'].values

total_genero = stats_masculino + stats_feminino
diferenca_real = stats_masculino - stats_feminino

icons = {
    'up': "tabler:arrow-up-right",
    'down': "tabler:arrow-down-right",
}

data = [
    {
        'label': 'Maculino', 
        'stats': stats_masculino,
        'progress': progress_masculino,
        'color': 'teal', 
        'icon': 'up'
    },
    {
        'label': 'Feminino',
        'stats': stats_feminino,
        'progress': progress_feminino,
        'color': 'blue',
        'icon': 'up'
    },
    {
        'label': 'DIFERENÇA REAL', 
        'stats': diferenca_real,
        'progress': (diferenca_real / total_genero * 100).round(2),
        'color': 'red',
        'icon': 'down'
    },
]

def StatsRing():
    stats = []
    for stat in data:
        Icon = icons[stat['icon']]
        stats.append(
            dmc.Paper(
                children=[
                    dmc.Group(
                        children=[
                            dmc.RingProgress(
                                size=80,
                                roundCaps=True,
                                thickness=8,
                                sections=[{'value': stat['progress'], 'color': stat['color']}],
                                label=dmc.Center(
                                    DashIconify(icon=Icon, width=20, height=20)
                                )
                            ),
                            dmc.Box(
                                children=[
                                    dmc.Text(stat['label'], c="dimmed", size="xs", tt="uppercase", fw=700),
                                    dmc.Text(stat['stats'], fw=700, size="xl"),
                                ]
                            )
                        ]
                    )
                ],
                withBorder=True,
                radius="md",
                p="xs",
            )
        )

    return dmc.SimpleGrid(
        children=stats,
        cols={"base": 1, "sm": 3},
        p="lg"
    )