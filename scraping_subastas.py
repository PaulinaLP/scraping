#Carga librerias
# -*- coding: utf-8 -*-
import pandas as pd
from urllib import request
import re

def scrape_subastas(url):
    # Inicializar DataFrame y contador
    col_names = ['tipo', 'subasta']
    my_df = pd.DataFrame(columns=col_names)
    a = 0

    # Iterar sobre los enlaces proporcionados
    for key, value in url.items():
        print(key)
        p = 0
        pestanha = str(p)
        fin = 0

        # Bucle hasta que se recorran todas las páginas de la subasta
        while fin == 0:
            try:
                print(a)
                # Construir la URL de la página de subasta
                url = value + pestanha + "-500"
                # Obtener el código fuente de la página
                sourceCode = str(request.urlopen(url).read().decode('ISO-8859-1'))
                start = 0
                seguir = 1
                pasoBucle = 0

                # Bucle para extraer los códigos de subasta de la página
                while seguir == 1:
                    match = re.search('SUBASTA SUB', sourceCode[start:])
                    if match:
                        m = match.start() + start
                        e = re.search('</h3>', sourceCode[m:(m + 70)])
                        end = e.start() + m
                        subasta = sourceCode[m:end]
                        new_row = pd.DataFrame.from_records({'tipo': [key], 'subasta': [subasta]})
                        my_df = pd.concat([my_df, new_row], ignore_index=True)
                        start = end
                        a = a + 1
                        pasoBucle = pasoBucle + 1
                    else:
                        seguir = 0
                        p = p + 500
                        pestanha = str(p)
                        if pasoBucle == 0:
                            fin = 1
            except:
                fin = 1

    # Extraer el código de subasta
    my_df['codigo_subasta'] = my_df['subasta'].apply(lambda x: x[8:] if ' ' not in x[8:] else x[8:x.find(' ', 9)].strip())

    return my_df

