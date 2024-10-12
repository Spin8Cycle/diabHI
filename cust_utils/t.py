from dash import dash_table, Dash, Input, Output, html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

sampling = ['No resampling (Original Data)', 'imblearn: RandomUnderSampler', 'imblearn: SMOTE']
text_style = {'color': 'white', 'fontSize': 14}

app.layout = html.Div([
    html.H4("Resampling Method "),
    dcc.Dropdown(sampling, id='sampler'),

    html.H4('Value Counts/Distribution Table'),
    html.P(id='table_out'),
    dash_table.DataTable(
        id='table',
        data = dist_table.to_dict('records'),
        columns = [{'name':i , "id":i}
                   for i in dist_table.columns],
        style_header={
                'textAlign':'center',
                'height': 'auto',
                'width': 'auto'
            },
        style_data={
                'textAlign':'center',
                'height': 'auto',
                'width': 'auto'
            }
        ),
])



@app.callback(
    Output("table_out", "children"), 
    Input("table", "active_cell")
    )
def display_color(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell['row'], active_cell['column_id']]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"



app.run(jupyter_mode='inline')