from process_data import *
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go

# archivo pensado para generar imágenes
def create_heatmap(df):
    heatmap_data = df.groupby(['Day of Week', 'Hour of Day']).agg(
        Patient_Count=pd.NamedAgg(column='Number of Records', aggfunc='sum'),
        Avg_Care_Score=pd.NamedAgg(column='Care Score', aggfunc='mean')
    ).reset_index()
    heatmap_count = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Patient_Count")
    heatmap_score = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Avg_Care_Score")
    tooltip_texts = [
        [
            f"<br>Calificación Promedio: {heatmap_score.iloc[i, j]:.2f}"
            if not pd.isna(heatmap_score.iloc[i, j]) else "No data"
            for j in range(len(heatmap_count.columns))
        ]
        for i in range(len(heatmap_count.index))
    ]
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_count = heatmap_count.reindex(days_order)
    ordered_tooltip_texts = [None] * len(days_order)
    current_days = list(heatmap_count.index)
    for i, day in enumerate(days_order):
        index = current_days.index(day)
        ordered_tooltip_texts[i] = tooltip_texts[index]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_count.values,
        x=heatmap_count.columns,
        y=heatmap_count.index,
        hoverongaps=False,
        colorscale='Viridis',
        hoverinfo='text',
        text=ordered_tooltip_texts 
    ))
    for i, day in enumerate(heatmap_count.index):
        for j, hour in enumerate(heatmap_count.columns):
            fig.add_annotation(
                x=hour,
                y=day,
                text=str(heatmap_count.at[day, hour]),
                showarrow=False,
                font=dict(color="white")
            )
    fig.update_layout(
        title='Volumen de Pacientes por Día y Hora',
        xaxis_title='Hora del Día',
        yaxis_title='Día de la Semana'
    )
    return fig

import plotly.graph_objects as go

def create_total_patients_graph(df):
    # Calcula la media móvil y la desviación estándar
    df['MA Total_Patients'] = df['Total_Patients'].rolling(window=7, min_periods=1).mean()
    df['STD Total_Patients'] = df['Total_Patients'].rolling(window=7, min_periods=1).std()

    # Calcula los límites superior e inferior de la banda de confianza
    confidence_interval = 1.96 * df['STD Total_Patients']  # 95% de confianza
    df['upper'] = df['MA Total_Patients'] + confidence_interval
    df['lower'] = df['MA Total_Patients'] - confidence_interval

    fig = go.Figure()
    
    # Diario
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Total_Patients'], mode='lines', name='Diario', line=dict(color='blue')))
    
    # Media Móvil
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA Total_Patients'], mode='lines', name='Media Móvil 7 días', line=dict(color='red')))
    
    # Banda de Confianza
    fig.add_trace(go.Scatter(
        x=df['Date'].tolist() + df['Date'].tolist()[::-1],
        y=df['upper'].tolist() + df['lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Banda de Confianza 95%'
    ))

    fig.update_layout(
        title='Total de Pacientes Diarios',
        xaxis_title='Fecha',
        yaxis_title='Total de Pacientes',
        plot_bgcolor='white',
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f")
    )
    return fig


def create_average_rating_graph(df):
    df['MA Avg_Care_Score'] = df['Avg_Care_Score'].rolling(window=7, min_periods=1).mean()
    df['STD Avg_Care_Score'] = df['Avg_Care_Score'].rolling(window=7, min_periods=1).std()

    confidence_interval = 1.96 * df['STD Avg_Care_Score']
    df['upper'] = df['MA Avg_Care_Score'] + confidence_interval
    df['lower'] = df['MA Avg_Care_Score'] - confidence_interval

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Avg_Care_Score'], mode='lines', name='Diario', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA Avg_Care_Score'], mode='lines', name='Media Móvil 7 días', line=dict(color='red')))
    fig.add_trace(go.Scatter(
        x=df['Date'].tolist() + df['Date'].tolist()[::-1],
        y=df['upper'].tolist() + df['lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Banda de Confianza 95%'
    ))

    fig.update_layout(
        title='Calificación Promedio Diaria',
        xaxis_title='Fecha',
        yaxis_title='Calificación Promedio',
        plot_bgcolor='white',
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f")
    )
    return fig


def create_average_wait_time_graph(df):
    df['MA Avg_Wait_Time'] = df['Avg_Wait_Time'].rolling(window=7, min_periods=1).mean()
    df['STD Avg_Wait_Time'] = df['Avg_Wait_Time'].rolling(window=7, min_periods=1).std()

    confidence_interval = 1.96 * df['STD Avg_Wait_Time']
    df['upper'] = df['MA Avg_Wait_Time'] + confidence_interval
    df['lower'] = df['MA Avg_Wait_Time'] - confidence_interval

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Avg_Wait_Time'], mode='lines', name='Diario', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA Avg_Wait_Time'], mode='lines', name='Media Móvil 7 días', line=dict(color='red')))
    fig.add_trace(go.Scatter(
        x=df['Date'].tolist() + df['Date'].tolist()[::-1],
        y=df['upper'].tolist() + df['lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Banda de Confianza 95%'
    ))

    fig.update_layout(
        title='Tiempo de Espera Promedio Diario',
        xaxis_title='Fecha',
        yaxis_title='Tiempo de Espera (minutos)',
        plot_bgcolor='white',
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f")
    )
    return fig
