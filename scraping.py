#Carga librerias
# -*- coding: utf-8 -*-
import datetime
import time
import pandas as pd
import urllib
import re 

# time started
started_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

# crea output
col_names = ['url','resultado','Titulo', 'Reg_Mercantil']
my_df = pd.DataFrame(columns=col_names)

# leer excel
df = pd.read_excel('input.xlsx')

search_items = df["url"].tolist()

#url = "https://www.sareb.es/es_ES/inmuebles/viviendas/SRB_HAYA_327617"

i=0

for item in search_items:
       
       #Duerme un segundo
       time.sleep(1)

       try:
               #Carga la pagina
               sourceCode = str(urllib.request.urlopen('https://www.einforma.com/servlet/app/prod/ETIQUETA_EMPRESA/nif/'+item).read().decode('ISO-8859-1'))
               print(sourceCode)
               resultado ='OK'
               
               try:
                       Titulo = sourceCode.split('le>')[1].split('<')[0]
               
               except:
                       Titulo = 'NA'
                       
               try:
                       Reg_Mercantil = sourceCode.split('cantil: <span class="bold">')[1].split('<')[0]
               
               except:
                       Reg_Mercantil = 'NA'
                       
               
       except:
               resultado = 'KO'
               Titulo = 'NA'
               Reg_Mercantil = 'NA'               
               
       i=i+1
    
       print(item + "-" + resultado + "-" + Titulo +"-" + Reg_Mercantil)
       
       my_df = my_df.append(pd.Series([item,resultado,Titulo,Reg_Mercantil], index=my_df.columns), ignore_index=True)
       if (i % 500== 0):
                my_df.to_excel("output.xlsx")
                print(i)

my_df.to_excel("output.xlsx")


