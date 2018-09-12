import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from queries import  query_datasets

app = dash.Dash()

app.layout = html.Div([

    html.H1("T E S S E R A C T"),

    html.H2("Exploring DataCubes"),

    dcc.Dropdown(
        id = "domain-list",
        options = query_datasets(),
        value = "tourism"
    ),

    html.Div(id = "target")
])


@app.callback(
    Output(component_id='target', component_property='children'),
    [Input(component_id='domain-list', component_property='value')]
)
def update_output_div(input_value):
    return f"You selected the {input_value} domain"


if __name__ == '__main__':
    app.run_server()