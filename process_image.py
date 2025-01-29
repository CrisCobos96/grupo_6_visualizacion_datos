from process_data import *
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go

# archivo pensado para generar imágenes
def create_heatmap(df):
    if df.empty:
        return go.Figure()
    
    try:
        heatmap_data = df.groupby(['Day of Week', 'Hour of Day']).agg(
            Patient_Count=pd.NamedAgg(column='Number of Records', aggfunc='sum'),
            Avg_Care_Score=pd.NamedAgg(column='Care Score', aggfunc='mean')
        ).reset_index()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_count = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Patient_Count")
        heatmap_score = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Avg_Care_Score")
        heatmap_count = heatmap_count.reindex(days_order).fillna(0)
        heatmap_score = heatmap_score.reindex(days_order).fillna(0)
        
        tooltip_texts = []
        for day in days_order:
            day_tooltips = []
            for hour in heatmap_count.columns:
                score = heatmap_score.at[day, hour] if day in heatmap_score.index else 0
                day_tooltips.append(
                    f"<br>Calificación Promedio: {score:.2f}" if score > 0 else "No data"
                )
            tooltip_texts.append(day_tooltips)
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_count.values,
            x=heatmap_count.columns,
            y=heatmap_count.index,
            hoverongaps=False,
            colorscale='Viridis',
            hoverinfo='text',
            text=tooltip_texts
        ))
        for i, day in enumerate(heatmap_count.index):
            for j, hour in enumerate(heatmap_count.columns):
                value = heatmap_count.at[day, hour]
                fig.add_annotation(
                    x=hour,
                    y=day,
                    text=str(int(value)) if value > 0 else "0",
                    showarrow=False,
                    font=dict(color="white")
                )
        fig.update_layout(
            title='Volumen de Pacientes por Día y Hora',
            xaxis_title='Hora del Día',
            yaxis_title='Día de la Semana'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error en create_heatmap: {str(e)}")
        return go.Figure()
import plotly.graph_objects as go

def create_total_patients_graph(df):
    df['MA Total_Patients'] = df['Total_Patients'].rolling(window=7, min_periods=1).mean()
    df['STD Total_Patients'] = df['Total_Patients'].rolling(window=7, min_periods=1).std()
    confidence_interval = 1.96 * df['STD Total_Patients']  
    df['upper'] = df['MA Total_Patients'] + confidence_interval
    df['lower'] = df['MA Total_Patients'] - confidence_interval
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Total_Patients'], mode='lines', name='Diario', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA Total_Patients'], mode='lines', name='Media Móvil 7 días', line=dict(color='red')))
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
