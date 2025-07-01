import dash_mantine_components as dmc
from dash import Dash, _dash_renderer

from components import layout
from components.callbacks import *

# Ensure React version compatibility
_dash_renderer._set_react_version("18.2.0")


app = Dash(external_stylesheets=dmc.styles.ALL)


app.layout = dmc.MantineProvider( 
    layout.body(),
    id="theme-provider",
)


if __name__ == "__main__":
    app.run(debug=True)
