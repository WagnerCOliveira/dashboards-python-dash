import matplotlib.pyplot as plt
import os
import pandas as pd
import plotly.express as px

from components.processamento import DataProcessing


class Figures(DataProcessing):
    
    def __init__(self, df):
        '''
        Define a pasta base
        Carrega o dataset
        '''        
        self.df = df


    def serie_temporal_data(self):
        return px.line(
            DataProcessing(df=self.df).series_temporal(),
            x='MES', 
            y='CONTAGEM',
            title='Série Temporal de Reclamações', 
            labels={'MES': 'Mês', 'CONTAGEM': 'Nº Reclamações'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))


    def freq_estado_data(self):
        return  px.bar(
            DataProcessing(df=self.df).data_estado(), 
            x='ESTADO', 
            y='count', 
            title='Reclamações por Estado', 
            labels={'ESTADO': 'Estado', 'count': 'Nº Reclamações'}, 
            text_auto=True
        ).update_xaxes(categoryorder="total descending").update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))


    def freq_status_data(self): 
        return px.pie(
            DataProcessing(df=self.df).data_status(),
            names='STATUS', 
            values='count', 
            title='Distribuição por Status', 
            hole=0.4
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))


    def freq_dist_texto(self): 
        return px.histogram(
            DataProcessing(df=self.df).data_texto(), 
            x='TAMANHO_TEXTO',             
            title='Distribuição do Tamanho do Texto',
            labels={'TAMANHO_TEXTO': 'Tamanho do Texto', 'count': 'Frequência'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=10, r=10, b=10))


    def map_data(self, ano_mapa):         
        
        return px.choropleth_mapbox(
            DataProcessing(df=self.df).data_mapa(ano_mapa=ano_mapa),
            geojson=DataProcessing.open_geo_json(), 
            locations='ESTADO', 
            featureidkey="properties.sigla",
            color='CONTAGEM', 
            color_continuous_scale="reds",
            mapbox_style="carto-positron", 
            zoom=3.2, 
            center={"lat": -14.2350, "lon": -51.9253},
            title=f'Reclamações em {ano_mapa}', 
            labels={'CONTAGEM': 'Nº Reclamações'}
        ).update_layout(title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))


    def freq_wordcloud(self):
        
        return DataProcessing(df=self.df).data_wordcloud()
        
        