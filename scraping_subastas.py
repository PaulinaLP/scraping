#Carga librerias
# -*- coding: utf-8 -*-
import datetime
import time
import pandas as pd
import urllib
import re 

# time started
started_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

col_names = ['tipo','subasta']
my_df = pd.DataFrame(columns=col_names)  

my_dic={'finalizada':"https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_aEZKMC80VWRPUjRsTXhTOUwxU3hpYllZVGF2M2JpVTI4bnZxajhhZVJseHVmRkZhTGRpRjI5OWovQW10WjNqSG5VcVJNcDY5clFPc29WOWFmVldKMlhDUHM4bTV1MGRnTjVPQ2ozUnNqZFhCeWZ2TGlkdkJCZm5Xd0hzUnVreDlDQ0o2T2ZCbE9RWkxsS2pvTnNLRktxdTY4Kzc0ZUorcGVVcWdsV0FNb0p3ZW1TcEJBaU9pSTFwL1ZGSmw4UU1jc2JWQnZIOUM4ZGlXemtrV2c2QUN3TFc4ZzJydTB0OUppUEZ3WmN3WlZtQThiQ2hBQmxCckxPVG4rNklveGlNWkxLMXdKbk9SY2lFNUNXdjdRcDFOSkZQeFJsZXpuaFViV3IxQnIrTUJJNUlRYUNkbllkei96OHJJcXBKWS9zbDFaRm1qampKRVpDNlIvN1Y4cktqOG1nPT0,-",
        'concluida':"https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_eFdFOEFWTUZlR2dEL3IzWVQ2eXJFZTdGOEFTbnN1ZWtveHUrbjVhcjhlejZTYklOMHcwa1hIYUNYM0ZHVDJzZWFEditXRWpvYjN1ZlhyemJZaXhOa25hSzIydnc5dkZ0cnZxRk9MK3ZOUlErbWVQSTRYdkZYRklZNjRUdktLQ1ZwM1hPU0IrTXJpWWtUL2I2REx3NDU5UFpVSW92WTdGTXJDQUV2UWIzQzRIbGlvRWRZSzZMbzhJUXdEU25BRlJOS0pjcDJwKytyMWg2TERjOXVQb3NFUW01SDEyUnBPVFJMK3hvdVFnVEM3RWxFTEoyYnFkazF1TEpFaWRJYzg4VDVuMnlPcjlIT3VQNVgzRVh2eUZHWTBMbW1hOHV5QUUva0ZadGFLbFM3OVZVNjczaS9jSjdTUnZhbzBqYmcwUHJYRXdURUZWQnlMOE5uS2NKTGFCSGN3PT0,-",
        'cancelada':"https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_eFdFOEFWTUZlR2dEL3IzWVQ2eXJFYWc4ZjFNbFlUYzBpcGVhd2M3VVRDUGxBcWVzOGloNHpQK0JsVlE2TmlLS1o4aDhtR2o4WDJyVkJ3em52Rno5bE1MMFJKQUU5TUU5bW5yWVBId0R1QTJ5eDU5UVN1N1hBMUlEUVVQeWo4NTZHWm9WOURVMjBXYkZGT2FWYVRoU2F1THJ6Wm41ZXFKQlJIRjliTHdiREE3Q3RlQUx5WUJkeHMrSks1UWp2TkRzUk8vT2VzWStoRGUyc0s5NlhkSVR2dWtIbEJzQnpvd1NNTnVsT0QzbXVReTJ2eGN0YTZlNkdvRXhyLy93WkF2Q3FORG0wYUVNeDlTR3VtcXBHQ2Z0cW1iR2JCREdCVkg2WlVKdzJuWGtMd0tJRVVRTFRxSDIzK3VwYkh0RzRKdUhTekZEb2NrR2N0TGJVeUE2U0QzUWxBPT0,-",
        'suspendida':"https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_aEZKMC80VWRPUjRsTXhTOUwxU3hpYmNGdXVtY242QXNNTERmeW1IQW02UFpaNitCd2ZHRlo1QUJ3Kzl5TXZvQnZOSVM0RmZQQTZzcmEwcUN4QW0rS0t0U1BES2V4cUpzTEd6Rm5HQ0dNR2JYa2dnejNmbmZsdnhXdFBMZmZ5aXB1Q3M4YitUL2FVVzNUcWN1WVFidmNWaHFwWmZkSjJKeXZqMDRGQzFyRDJiWlhBZHFaWHF3MlhkL21BQyt6bmNwbVB3eHJhSGxteU5taGtIbVlOZ04wWks5TStLU01kRGYyZnpYWVhNZmNDWXR2dzBUTWM4R1VLcFJEeVN0MzlyVFRsMU4rN3VqYzJ3SDBrSG9NQTVGbnlMSWFPZTNVTjhyWE1saGRPdXA1VXp2a1FsOEo2TFBzYmc1UVpPdFdRV2REeCt1SWM4L0FqeDJIelJQTllGc01nPT0,-"}

#finalizada por autoridad gestora
#"https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_aEZKMC80VWRPUjRsTXhTOUwxU3hpUm44VGdpRHZFZWV1MnYzWDFVODZEK3JGN1dKdW9wUi9PN3BTSndoQVpJMzdvd29tdExRb3U3Mnk0MG9zMHpCMW05OU41VjBaNEVPeGluY090anBEM2FUMEpTNE4vUE5VcVY3aitNSmZtRkMyaHN2VDFCenhEL2dTakl1a1FKblAwbU9Vb1dKVGtUcnFSQ2V4aDRpdVlrUDVZRTJwQWp0SnhxTUttV2svOUoyckRYc29hVnVsUXMwWjhzWGVJMEZ4WDQ5NU01QUJhSUxBelE2YXptYXhCYjVsNmdPTkFaQ1ZXMXdqRnhKbnRnYzRZNCtkcmxkSVFsL1JHK2ZBYTgxdGJZck5YK1RtR2RtWE14TFZYbW44ajRFUGU2K2IxUWU2NXRORkxCZzhuV3YyLy9aSm9iZE1PSG1sNkc2dXRocnhRPT0,-"+pestanha+"-500"
a=0
for key,value in my_dic.items():
    print(key)
    p=0
    pestanha=str(p)
    fin=0
    #este bucle recorre todas las pestañas de un tipo de finalizacion
    while fin==0:
        try:
            #Carga la pagina
            print(a)
            url = value+pestanha+"-500"
            sourceCode = str(urllib.request.urlopen(url).read().decode('ISO-8859-1'))        
            print(url)                      
            start=0
            seguir=1
            pasoBucle=0
            #este bucle recorre el codigo fuente y apunta todos los codigos de subasta
            while seguir==1:
                match=re.search('SUBASTA SUB',sourceCode[start:])     
                if match:
                    m=match.start()+start
                    e=re.search('</h3>',sourceCode[m:(m+70)]) 
                    end=e.start()+m
                    subasta=sourceCode[m:end] 
                    new_row = pd.DataFrame.from_records({'tipo': [key], 'subasta':[subasta]})   
                    #guardo codigo subasta y tipo en el df
                    my_df = pd.concat([my_df,new_row], ignore_index=True)   
                    start=end  
                    a=a+1
                    pasoBucle=pasoBucle+1
                else:
                    #cuando he recogido todos los codigos voy a la siguiente pestaña
                    seguir=0     
                    p=p+500 
                    pestanha=str(p)
                    #si no he encontrado en la pestaña ningun codigo voy al siguiente tipo
                    if pasoBucle==0:
                        fin=1                       
        except:
             fin=1 
my_df['codigo_subasta'] = my_df['subasta'].apply(lambda x: x[8:] if ' ' not in x[8:] else x[8:x.find(' ', 9)].strip())        

my_df.to_excel("output.xlsx",index=False)


