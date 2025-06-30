import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, _dash_renderer

from components import layout

# Ensure React version compatibility
_dash_renderer._set_react_version("18.2.0")


app = Dash(external_stylesheets=dmc.styles.ALL)


app.layout = layout.body()


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
