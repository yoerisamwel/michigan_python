import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

#data cleaning
df = pd.read_csv("data.csv")

df_2 = df.groupby('fc').sum().reset_index()
print(df_2)
bar_1 = px.bar(df_2, x="fc", y="orders", color="fc")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(['Total shipments per FC'], style={'font-weight': 'bold', "text-align": "center"}),
    html.Div(dcc.Graph(figure=bar_1)),
    html.Br(),
    html.Div([
        html.Label(['Choose category:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='dropdown_fc',
                         options=[
                             {'label': 'Baltimore', 'value': 'Baltimore'},
                             {'label': 'DC', 'value': 'Washington D.C.'},
                             {'label': 'Manhattan', 'value': 'Manhattan'}
                         ],
                         optionHeight=35,  # height/space between dropdown options
                         value='Baltimore',  # dropdown value selected automatically when page loads
                         disabled=False,  # disable dropdown value selection
                         multi=False,  # allow multiple dropdown values to be selected
                         searchable=True,  # allow user-searching of dropdown values
                         search_value='',  # remembers the value searched in dropdown
                         placeholder='Please select...',  # gray, default text shown when no option is selected
                         clearable=True,  # allow user to removes the selected value
                         style={'width': "40%"},  # use dictionary to define CSS styles of your dropdown
                         # className='select_box',           #activate separate CSS document in assets folder
                         # persistence=True,                 #remembers dropdown value. Used with persistence_type
                         # persistence_type='memory'         #remembers dropdown value selected until...
                         ),  # 'memory': browser tab is refreshed
            # 'session': browser tab is closed
            # 'local': browser cookies are deleted
        ]),

    html.Br(),
    html.Div(id='Bar1'),
    html.Br(),
    html.Div(id='cholro_1')

    ])

#callbacks


@app.callback(
    Output(component_id='Bar1', component_property='children'),
    Input(component_id='dropdown_fc', component_property='value'))

def build_graph_1(value):
    df_graph = df.copy()[df['fc'] == value]

    fig_bar_1 = px.bar(df_graph,
                        x="recipient_state",
                        y="orders",
                        hover_name="recipient_state")
    fig_bar_1.update_layout(
        title_text='Total Shipments for selected FC per State',
        geo_scope='usa',  # limit map scope to USA
        height=600,
        width=1750
    )

    return [dcc.Graph(id='Bar1_v1', figure=fig_bar_1)]


@app.callback(
    Output(component_id='cholro_1', component_property='children'),
    Input(component_id='dropdown_fc', component_property='value')
    )

def build_graph_2(value):
    df_graph = df.copy()[df['fc'] == value]

    fig = go.Figure(data=go.Choropleth(
        locations=df_graph['recipient_state'],  # Spatial coordinates
        z=df_graph['orders'].astype(float),  # Data to be color-coded
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="shipment_sum",
    ))
    fig.update_layout(
        title_text='Total Shipments per State',
        geo_scope='usa',  # limit map scope to USA
        height=600,
        width=1750
    )

    return [dcc.Graph(id='Chloro_graph_1', figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=True)