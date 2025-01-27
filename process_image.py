from process_data import *
import pandas as pd
import plotly.express as px
import dash


# archivo pensado para generar imágenes
def create_heatmap(df=read_documents()):
    heatmap_data = df.groupby(['Day of Week', 'Hour of Day']).agg(
        Patient_Count=pd.NamedAgg(column='Number of Records', aggfunc='sum'),
        Avg_Care_Score=pd.NamedAgg(column='Care Score', aggfunc='mean')
    ).reset_index()
    heatmap_count = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Patient_Count")
    heatmap_score = heatmap_data.pivot(index="Day of Week", columns="Hour of Day", values="Avg_Care_Score")

    # Crear los textos para los tooltips
    tooltip_texts = [
        [
            f"<br>Calificación Promedio: {heatmap_score.iloc[i, j]:.2f}"
            if not pd.isna(heatmap_score.iloc[i, j]) else "No data"
            for j in range(len(heatmap_count.columns))
        ]
        for i in range(len(heatmap_count.index))
    ]
    # Orden explícito para los días de la semana
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Reordenar el DataFrame por días de la semana
    heatmap_count = heatmap_count.reindex(days_order)

    # Reordenar manualmente la lista tooltip_texts según days_order
    # Asumiendo que tooltip_texts es una lista de listas donde cada sublista corresponde a un día
    ordered_tooltip_texts = [None] * len(days_order)
    current_days = list(heatmap_count.index)

    for i, day in enumerate(days_order):
        index = current_days.index(day)
        ordered_tooltip_texts[i] = tooltip_texts[index]

    # Ahora crea el mapa de calor con el orden correcto
    import plotly.graph_objects as go

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_count.values,
        x=heatmap_count.columns,
        y=heatmap_count.index,
        hoverongaps=False,
        colorscale='Viridis',
        hoverinfo='text',
        text=ordered_tooltip_texts  # Usar la lista reordenada
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

    # Añadir título y etiquetas
    fig.update_layout(
        title='Volumen de Pacientes por Día y Hora',
        xaxis_title='Hora del Día',
        yaxis_title='Día de la Semana'
    )

    # Mostrar la figura
    fig.show()
