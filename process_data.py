import pandas as pd
import numpy as np 
import plotly.express as px

# archivo para procesamiento, lectura y filtrado de dataframes
members=[{"name": "Alisson Monserratte López Mejía"},
         {"name":"Diana Carolina Ortiz Pillajo"},{"name":"Maria Jose Villavicencio Proaño"},{"name":"Cristhian Nahim Cobos Morales"}]

members_col=[{"name":"Nombre", "id":"name"}]

def read_documents():
    df=pd.read_csv('./clinical_analytics.csv')
    df['Appt Start Time'] = pd.to_datetime(df['Appt Start Time'],format='%Y-%m-%d %I:%M:%S %p')
    df['Day of Week'] = df['Appt Start Time'].dt.day_name()
    df['Hour of Day'] = df['Appt Start Time'].dt.hour
    df['Date'] = df['Appt Start Time'].dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def card_information(df):
    total_patients = df['Number of Records'].sum()
    average_care_score = df['Care Score'].mean()
    return total_patients,average_care_score

