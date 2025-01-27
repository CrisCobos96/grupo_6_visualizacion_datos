from process_data import *
from process_image import *
from dash import Dash, html,dcc,dash_table
import dash_bootstrap_components as dbc
# crea la visualizacion 
external_stylesheets=[dbc.themes.BOOTSTRAP,
                      'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']

app= Dash(__name__, external_stylesheets=external_stylesheets)

app. layout= html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Análisis de visitas Médicas en Hospitales",className="text-center mb-4",style={'color': '#8681F5'}))
        ]),
        dbc.Row([
            dbc.Col(html.P("En este dashboard encontrarás un análisis detallado de los datos genrados en las visitas médicas en un hospital ... (se debe mejorar)",
                           className="text-center"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Accordion([
                    dbc.AccordionItem(title=html.Div([html.I(className="fas fa-info-circle mr-2"),"Integrantes del Grupo 6"]),
                                      children=[html.P("A continuación, se muestra la lista de integrantes:"),
                                                dash_table.DataTable(
                                                    data=members,
                                                    columns=members_col,
                                                    style_cell={'textAlign':'left'},

                                                    style_header={
                                                        'backgroundColor':'rgb(210,210,210)', 'fontWeight':'bold'
                                                    },
                                                    style_data={
                                                        'backgroundColor':'rgb(210,210,210)', 'color':'black'
                                                    }
                                                )
                                                ])
                ])
            ])
        ])
    ])

])

app.run_server(debug=True)