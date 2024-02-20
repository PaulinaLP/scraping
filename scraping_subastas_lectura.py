# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:01:16 2023

@author: AAM01379H
"""
import datetime
import time
import pandas as pd
import urllib
import re 
from html import unescape
import pickle
import numpy as np

def extract_lotes(input_string):
    pattern = r'\((\d+) lotes\)'
    match = re.search(pattern, input_string)
    return int(match.group(1)) if match else None

df=pd.read_excel("output.xlsx")
df['lotes']=df['subasta'].apply(extract_lotes)
df['lotes']=df['lotes'].fillna(0)
df['lotes']=df['lotes'].astype(int)
dfLotes=pd.DataFrame(columns=['codigo_subasta','lote'])
dfLotes.set_index(['codigo_subasta', 'lote'], inplace=True)

b = 200
#este bucle recorre todas las subastas
df=df[df['lotes']!=0]
df=df.reset_index(drop=True)

for index, row in df.iterrows():
    codigo=row['codigo_subasta']     
    if index % b ==0:
        print(index)   
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    #este bucle recorre todas las pestañas
    if row['lotes']==0:         
        for ver in [1,2,3,4,5,6]:
            try:
                url="https://subastas.boe.es/detalleSubasta.php?idSub="+codigo+"&ver="+str(ver)
                sourceCode = str(urllib.request.urlopen(url).read().decode('utf-8'))   
                sourceCode = unescape(sourceCode)
                #print(ver)            
                start=0
                seguir=1            
                #este bucle recorre el codigo fuente y apunta todos los datos de substa
                while seguir==1:
                    match=re.search('<th>',sourceCode[start:])     
                    if match:
                        m=match.start()+start
                        e=re.search('</th>',sourceCode[m:(m+100)]) 
                        end=e.start()+m
                        columna=sourceCode[(m+4):end] 
                        posValor=re.search('<td>',sourceCode[end:]) 
                        posValorStart=posValor.start()+end
                        posValor2=re.search('</td>',sourceCode[posValorStart:]) 
                        posValorEnd=posValor2.start()+posValorStart
                        valor=sourceCode[(posValorStart+4):posValorEnd] 
                        start=end                                        
                        df.at[index, columna+str(ver)] = valor                    
                        #print(f'{columna}{valor}')
                    else:
                        #cuando he recogido todos los datos va a la siguiente pestaña
                        seguir=0     
            except:
                pass
    else:
        for lote in range(1,row['lotes']+1):
            fila=0       
            for ver in [1,2,3,4,5,6]:
                try:  
                    url="https://subastas.boe.es/detalleSubasta.php?idSub="+codigo+"&ver="+str(ver)+"&idLote="+str(lote)
                    sourceCode = str(urllib.request.urlopen(url).read().decode('utf-8'))   
                    sourceCode = unescape(sourceCode)
                    #print(ver)            
                    start=0
                    seguir=1            
                    #este bucle recorre el codigo fuente y apunta todos los datos de substa                    
                    while seguir==1:
                        match=re.search('<th>',sourceCode[start:])     
                        if match:
                            m=match.start()+start
                            e=re.search('</th>',sourceCode[m:(m+100)]) 
                            end=e.start()+m
                            columna=sourceCode[(m+4):end] 
                            posValor=re.search('<td>',sourceCode[end:]) 
                            posValorStart=posValor.start()+end
                            posValor2=re.search('</td>',sourceCode[posValorStart:]) 
                            posValorEnd=posValor2.start()+posValorStart
                            valor=sourceCode[(posValorStart+4):posValorEnd] 
                            start=end  
                            if fila==0:
                                data = [{'codigo_subasta': row['codigo_subasta'], 'lote': lote}]                            
                                new_row = pd.DataFrame(data)
                                new_row.set_index(['codigo_subasta', 'lote'], inplace=True) 
                                dfLotes = pd.concat([dfLotes,new_row])                                                                
                            dfLotes.at[(row['codigo_subasta'], lote), columna+str(ver)] = valor 
                            fila=fila+1
                            #print(f'{columna}{valor}')
                        else:
                            #cuando he recogido todos los datos va a la siguiente pestaña
                            seguir=0     
                except:
                    pass

dFin=df.copy()
dfLotesFin=dfLotes.copy()

def extract_text(html_content):
    try:
        match = re.search(r'<strong>(.*?)<\/strong>', html_content)        
    except:
        match=False
    return match.group(1) if match else None
def extract_text2(html_content):
    try:
        match = re.search(r'<strong class="destaca">(.*?)<\/strong>', html_content)
    except:
        match=False
    return match.group(1) if match else None
def convertNum (amount_string):
    try:
        numeric_string = ''.join(char for char in str(amount_string) if char.isdigit() or char in {','})
        numeric_string = numeric_string.replace(',', '.')
        numeric_value = float(numeric_string)
    except:
        numeric_value=None
    return numeric_value

dFin.columns
# Apply the function to the DataFrame column
def transformacion(dFin):
    dFin['Tipo de subasta1'] = dFin['Tipo de subasta1'].apply(extract_text)
    dFin['Identificador1'] = dFin['Identificador1'].apply(extract_text)
    dFin['Fecha de inicio1'] = dFin['Fecha de inicio1'].apply(lambda x:str(x)[:10])
    dFin['Fecha de conclusión1'] = dFin['Fecha de conclusión1'].apply(extract_text2)
    dFin['Fecha de conclusión1'] = dFin['Fecha de conclusión1'].apply(lambda x:str(x)[:10])  
    for columna in ['Cantidad reclamada1',  'Valor subasta1',
    'Tasación1', 'Tramos entre pujas1', 'Importe del depósito1']:
        dFin[columna]=dFin[columna].apply(convertNum)
    return dFin

dFin=transformacion(dFin)
dfLotesFin=transformacion(dfLotesFin)
dfLotesFin=dfLotesFin.reset_index()

dFin.to_excel('lectura_subastas.xlsx')
dfLotesFin.to_excel('lectura_subastas_lotes.xlsx')

with open('lectura_subastas.pkl', 'wb') as f:
    pickle.dump(df, f)
with open('lectura_subastas_lotes.pkl', 'wb') as f:
    pickle.dump(dfLotesFin, f)

    
#check por si hay mas de 1 bien por subasta
sinLotes=df[df['lotes']==0]
sinLotes=sinLotes[['codigo_subasta']]
sinLotes=sinLotes.reset_index(drop=True)
b=200
for index, row in sinLotes.iterrows():
    codigo=row['codigo_subasta']     
    if index % b ==0:
        print(index)   
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))        
    try:
        url="https://subastas.boe.es/detalleSubasta.php?idSub="+codigo+"&ver="+str(3)
        sourceCode = str(urllib.request.urlopen(url).read().decode('utf-8'))   
        sourceCode = unescape(sourceCode)
        #print(ver)            
        start=0
        seguir=1    
        numB=0
        #este bucle recorre el codigo fuente y apunta todos los datos de substa
        while seguir==1:
            match=re.search('<h4>',sourceCode[start:])     
            if match:
                numB= numB+1
                m=match.start()+start
                end=m+3
                start=end   
            else:
                #cuando he recogido todos los datos va a la siguiente pestaña
                seguir=0    
        df.at[index, 'numB'] = numB
    except:
        pass
a=df[['numB']]
c=pd.merge(sinLotes,a,how='inner',left_index=True,right_index=True)
c.to_excel('numBienes.xlsx')