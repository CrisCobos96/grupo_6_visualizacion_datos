from process_data import *
from process_image import *
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

df = read_documents()
#df['Clinic Name'] = df['Clinic Name'].astype(str)
#df['Department'] = df['Department'].astype(str)
#df['Appt Start Time'] = pd.to_datetime(df['Appt Start Time'])  
default_clinic =[ df['Clinic Name'].iloc[0]]
default_department =[ df['Department'].iloc[0]]  
default_start_date = df['Appt Start Time'].min()  
default_end_date = df['Appt Start Time'].max()  
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Análisis de visitas Médicas en Hospitales", className="text-center mb-4", style={'color': '#8681F5'}))
        ]),
        dbc.Row([
            dbc.Col(html.P("En este dashboard encontrarás un análisis detallado de los datos generados en las visitas médicas en un hospital.",
                           className="text-center"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Accordion([
                    dbc.AccordionItem(
                        title=html.Div([html.I(className="fas fa-info-circle mr-2"), "Integrantes del Grupo 6"]),
                        children=[
                            html.P("A continuación, se muestra la lista de integrantes:"),
                            dash_table.DataTable(
                                data=members,  # Asegúrate de que esta variable está bien definida con los datos de los miembros
                                columns=members_col,  # Asegúrate de que esta variable está bien definida con las columnas adecuadas
                                style_cell={'textAlign': 'left'},
                                style_header={
                                    'backgroundColor': 'rgb(210,210,210)', 
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'rgb(240,240,240)', 
                                    'color': 'black'
                                }
                            )
                        ]
                    )
                ])
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='clinic-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Clinic Name'].unique()],
                    placeholder="Seleccione una clínica",
                    multi=True,
                    value=default_clinic
                )],width=4),
                dbc.Col([
                dcc.Dropdown(
                    id='department-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Department'].unique()],
                    placeholder="Seleccione un departamento",
                    multi=True,
                    value=default_department
                )],width=4),
                dbc.Col([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=default_start_date,
                    end_date=default_end_date,
                    display_format='YYYY-MM-DD'
                )
            ],width=4)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='heatmap-graph')
            ], width=12)
        ]),
        html.H2("Indicadores Clave de Rendimientos", className="mt-4 mb-4"),
                dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total de Pacientes", className="card-title"),
                        html.P(id="total-patients-kpi", className="card-text")
                    ]),
                    dcc.Graph(id='total-patients-graph')
                ], style={"width": "100%"})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Calificación Promedio", className="card-title"),
                        html.P(id="average-rating-kpi", className="card-text")
                    ]),
                    dcc.Graph(id='average-rating-graph')
                ], style={"width": "100%"})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Tiempo de Espera Promedio", className="card-title"),
                        html.P(id="average-wait-time-kpi", className="card-text")
                    ]),
                    dcc.Graph(id='average-wait-time-graph')
                ], style={"width": "100%"})
            ], width=12)
        ])
    ])
])

@app.callback(
    [Output('heatmap-graph', 'figure'),
    Output('total-patients-graph', 'figure'),
    Output('average-rating-graph', 'figure'),
    Output('average-wait-time-graph', 'figure'),
    Output('total-patients-kpi', 'children'),
    Output('average-rating-kpi', 'children'),
    Output('average-wait-time-kpi', 'children')
     ],
    [Input('clinic-dropdown', 'value'),
     Input('department-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(selected_clinics, selected_departments, start_date, end_date):
    if not selected_clinics or not selected_departments or not start_date or not end_date:
        
        return [{}]
    filtered_df = df[(df['Clinic Name'].isin(selected_clinics)) & (df['Department'].isin(selected_departments)) &
                     (df['Appt Start Time'] >= pd.to_datetime(start_date)) & (df['Appt Start Time'] <= pd.to_datetime(end_date))]
    df_daily = df.groupby('Date').agg(
    Total_Patients=pd.NamedAgg(column='Number of Records', aggfunc='size'),
    Avg_Care_Score=pd.NamedAgg(column='Care Score', aggfunc='mean'),
    Avg_Wait_Time=pd.NamedAgg(column='Wait Time Min', aggfunc='mean')).reset_index()

    heatmap_fig = create_heatmap(filtered_df)
    fig1 = create_total_patients_graph(df_daily)
    fig2 = create_average_rating_graph(df_daily)
    fig3 = create_average_wait_time_graph(df_daily)
    total_patients = filtered_df['Number of Records'].sum()
    average_rating = filtered_df['Care Score'].mean()
    average_wait_time = filtered_df['Wait Time Min'].mean()
    return [heatmap_fig,fig1, fig2, fig3, f"{total_patients} pacientes", f"{average_rating:.2f}", f"{average_wait_time:.2f} minutos"]

app.run_server(debug=True)
