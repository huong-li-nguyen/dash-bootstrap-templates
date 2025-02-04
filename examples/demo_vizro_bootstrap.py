"""
This is a demo of the `vizro.bootstrap` theme combined with the load_figure_template(themes) function
from dash_bootstrap_templates.py

Unlike other Bootstrap themes, the `vizro.bootstrap` theme is not included in the `dbc.themes` module and
must be imported from the `vizro` module.

The `load_figure_template` function behaves as expected: it loads the Bootstrap theme, adds it to `plotly.io`,
and sets it as the default.
"""
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
import vizro

from dash_bootstrap_templates import load_figure_template

# Load data and figure templates
gapminder = px.data.gapminder().query("year==2007")
load_figure_template(["vizro", "vizro_dark"])

# Create components for the dashboard
color_mode_switch = dbc.Switch(
    id="switch", value=False, persistence=True, label="Switch between dark and light!", className="mt-4"
)
scatter = dcc.Graph(
    id="scatter", figure=px.scatter(gapminder, x="gdpPercap", y="lifeExp", size="pop", size_max=60, color="continent")
)
box = dcc.Graph(id="box", figure=px.box(gapminder, x="continent", y="lifeExp", color="continent"))


tabs = dbc.Tabs(
    [
        dbc.Tab(scatter, label="Scatter Plot"),
        dbc.Tab(box, label="Box Plot"),
    ]
)

# Initiate app
app = Dash(__name__, external_stylesheets=[vizro.bootstrap])
app.layout = dbc.Container(
    [html.H1("Vizro Bootstrap Demo", className="bg-primary p-2 mt-4"), color_mode_switch, tabs],
    fluid=True,
)


# Add callbacks to switch between dark / light
@callback(
    [Output("scatter", "figure"), Output("box", "figure")],
    Input("switch", "value"),
)
def update_figure_template(switch_on):
    """Sync the figure template with the color mode switch on the bootstrap template."""
    template = pio.templates["vizro"] if switch_on else pio.templates["vizro_dark"]
    patched_figure = Patch()
    patched_figure["layout"]["template"] = template

    return patched_figure, patched_figure


clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)


if __name__ == "__main__":
    app.run(debug=True)
