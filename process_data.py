import pandas as pd
import numpy as np 

# archivo para procesamiento, lectura y filtrado de dataframes
members=[{"name": "Integrante 1"},
         {"name":"Integrante 2"},{"name":"Integrante 3"},{"name":"Integrante 4"}]

members_col=[{"name":"Nombre", "id":"name"}]

def read_documents():
    df=pd.read_csv('./clinical_analytics.csv')
    df['Appt Start Time'] = pd.to_datetime(df['Appt Start Time'])
    df['Day of Week'] = df['Appt Start Time'].dt.day_name()
    df['Hour of Day'] = df['Appt Start Time'].dt.hour
    # agregar tratamiento de datos
    return df

