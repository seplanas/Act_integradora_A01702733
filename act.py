from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import time

# logo
st.image('SFPD.png')

st.title('Police incident reports from 2018 to 2020 in San Francisco👮')

df = pd.read_csv('Police.csv')
df.sample(n=50000, random_state=42)
    
st.markdown('The data shown below belongs to incident reports in the City of San Francisco, from the year 2018 to 2020, woth details from each case such as date, day of the week, police district, neighbourhood in which it happened, type of incident in category and subcategory, exact location and resolution')

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['District'] = df['Police District']
mapa['Neighbourhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()
    

subset_data3 = mapa
neighbourhood_input = st.sidebar.multiselect('District',
                                         subset_data3.groupby('District').count().reset_index()['District'].tolist())
if len(neighbourhood_input) > 0:
    subset_data3 = subset_data3[subset_data3['District'].isin(neighbourhood_input)]

subset_data2 = subset_data3
incident_input = st.sidebar.multiselect('Neighbourhood',
                                        subset_data3.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
if len(incident_input) > 0:
    subset_data2 = subset_data3[subset_data3['Neighbourhood'].isin(incident_input)]

subset_data1 = subset_data2
incident_sub_input = st.sidebar.multiselect('Incident Category',
                                        subset_data2.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_sub_input) > 0:
    subset_data1 = subset_data2[subset_data2['Incident Category'].isin(incident_sub_input)]

subset_data = subset_data1
resolution_input = st.sidebar.multiselect('Incident Subcategory',
                                        subset_data1.groupby('Incident Subcategory').count().reset_index()['Incident Subcategory'].tolist())
if len(resolution_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Subcategory'].isin(resolution_input)]    

count = subset_data['Neighbourhood'].nunique()
count_1 = subset_data['District'].nunique()

st.markdown('cuenta de vecindarios y distritos que hay en la zona')

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="background-color: {'#00288f'}; padding: 20px; border-radius: 10px;">
            <p style="color: white;">
                Número de vecindarios: {count} <br>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color: {'#0640ae'}; padding: 20px; border-radius: 10px;">
            <p style="color: white;">
                Número distritos: {count_1} <br>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

subset_data

with st.spinner('Loading data...'):
    time.sleep(5)

st.markdown('It is important to mention that any police district can answer to any incident, the neighbourhood in which it happened is not related to the police district')
st.markdown('Crime locations in San Francisco')

fig_density = px.density_mapbox(mapa, 
                        lat='lat', 
                        lon='lon', 
                        radius=8, 
                        center=dict(lat=mapa['lat'].mean(), lon=mapa['lon'].mean()),
                        zoom=12,
                        mapbox_style='open-street-map', 
                        title='Mapa de calor')

fig_density.update_layout(margin=dict(b=0, t=0, l=0, r=0))
st.plotly_chart(fig_density)

st.markdown('Crimes ocurred per day of the week')
label = subset_data['Day'].unique()
colores = ['#00288f','#0640ae','#0859ce', '#0573ee', '#448fff', '#76aeff', '#9aceff']
count10 = subset_data['Neighbourhood'].value_counts()
fig_pie = go.Figure(data=[go.Pie(labels=label, values=count10, marker=dict(colors=colores))])
st.plotly_chart(fig_pie)
st.markdown('Crimes ocurred per date')
st.bar_chart(subset_data['Date'].value_counts())
st.markdown('Types of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts())

agree = st.button('Click to see incident subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

st.markdown('Resolution status')
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=90, colors=colores)
st.pyplot(fig1)


st.markdown('### Vecindarios desglosados por incidentes')
st.markdown('Aquí se usan 5 tipos de incidentes que creo que pueden ser importantes para las personas que usen el tablero')

categorias_deseadas = ['Assault', 'Homicide', 'Vandalism', 'Embezzlement', 'Weapons Offence']

mapa_filtrado = mapa[mapa['Incident Category'].isin(categorias_deseadas)]

fig_bar = px.bar(
    mapa_filtrado,
    x='Neighbourhood',
    hover_name='Incident Category',
    hover_data=['Incident Subcategory', 'Resolution'],
    color='Incident Category',
    color_discrete_map={category: color for category, color in zip(mapa_filtrado['Incident Category'].unique(), colores)}
)
fig_bar.update_layout(height=600, width=1000)

st.plotly_chart(fig_bar)

