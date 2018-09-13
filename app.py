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

    html.Div(id = "target"),

    html.H2("I want to take a look at :"), 

    dcc.RadioItems(
        id = "select-dim-or-meas",
        options=[
            {'label': 'Dimensions', 'value': 'dimensions'},
            {'label': 'Measures', 'value': 'measures'}
        ],
        value=''
        ),
    
    html.Div(id = "table")
    
])

# ----- Callbacks
@app.callback(
    Output(component_id='target', component_property='children'),
    [Input(component_id='domain-list', component_property='value')]
)
def update_output_div(input_value):
    return f"You selected the {input_value} domain"

@app.callback(
    Output(component_id = "table", component_property = "children"),
    [Input(component_id = "select-dim-or-meas", component_property = "value")]
)
def get_dimensions_or_measures(input_value):
    if (input_value == "dimensions"):
        # TODO use the request
        return html.Table ([html.Tr([html.Td("yo")]) for row in range(10)])
    elif (input_value == "measures"):
        return html.Table ([html.Tr([html.Td("test")]) for row in range(10)])
    else:
        return html.Div("No dimensions or measures chosen")


if __name__ == '__main__':
    app.run_server()