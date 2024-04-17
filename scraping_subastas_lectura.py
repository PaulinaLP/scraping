import datetime
import re
import time
from html import unescape
from urllib import request

import pandas as pd


# Función para extraer el número de lotes de la descripción de la subasta
def extract_lotes(input_string):
    pattern = r'\((\d+) lotes\)'
    match = re.search(pattern, input_string)
    resultado = int(match.group(1)) if match else 0
    return resultado


# Función para extraer el texto entre etiquetas <strong>
def extract_text(html_content):
    try:
        match = re.search(r'<strong>(.*?)<\/strong>', html_content)
    except:
        match = False
    return match.group(1) if match else None


# Función para extraer el texto entre etiquetas <strong class="destaca">
def extract_text2(html_content):
    try:
        match = re.search(r'<strong class="destaca">(.*?)<\/strong>', html_content)
    except:
        match = False
    return match.group(1) if match else None


# Función para convertir cadenas de texto con cantidades numéricas a números
def convertNum(amount_string):
    try:
        numeric_string = ''.join(char for char in str(amount_string) if char.isdigit() or char in {','})
        numeric_string = numeric_string.replace(',', '.')
        numeric_value = float(numeric_string)
    except:
        numeric_value = None
    return numeric_value


# Función para transformar el DataFrame principal
def transformacion(df):
    df['Tipo de subasta1'] = df['Tipo de subasta1'].apply(extract_text)
    df['Identificador1'] = df['Identificador1'].apply(extract_text)
    df['Fecha de inicio1'] = df['Fecha de inicio1'].apply(lambda x: str(x)[:10])
    df['Fecha de conclusión1'] = df['Fecha de conclusión1'].apply(extract_text2)
    df['Fecha de conclusión1'] = df['Fecha de conclusión1'].apply(lambda x: str(x)[:10])
    for columna in ['Cantidad reclamada1', 'Valor subasta1', 'Tasación1', 'Tramos entre pujas1',
                    'Importe del depósito1']:
        try:
            df[columna] = df[columna].apply(convertNum)
        except:
            pass
    return df

def lectura():
    # Lectura del archivo de entrada
    df = pd.read_excel("output\output.xlsx")

    # Extracción del número de lotes
    df['lotes'] = df['subasta'].apply(extract_lotes)

    # DataFrame para almacenar los datos de los lotes
    dfLotes = pd.DataFrame(columns=['codigo_subasta', 'lote'])

    # Cantidad de filas a procesar en cada iteración
    batch_size = 200

    for index, row in df.iterrows():
        codigo = row['codigo_subasta']

        if index % batch_size == 0:
            print(index)
            print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        # Si la subasta no tiene lotes
        if row['lotes'] == 0:
            for ver in range(1, 7):
                try:
                    url = "https://subastas.boe.es/detalleSubasta.php?idSub=" + codigo + "&ver=" + str(ver)
                    sourceCode = str(request.urlopen(url).read().decode('utf-8'))
                    sourceCode = unescape(sourceCode)
                    print(url)
                    start = 0
                    seguir = 1

                    # Recorrido del código fuente y extracción de los datos de la subasta
                    while seguir == 1:
                        match = re.search('<th>', sourceCode[start:])
                        if match:
                            m = match.start() + start
                            e = re.search('</th>', sourceCode[m:(m + 100)])
                            end = e.start() + m
                            columna = sourceCode[(m + 4):end]
                            posValor = re.search('<td>', sourceCode[end:])
                            posValorStart = posValor.start() + end
                            posValor2 = re.search('</td>', sourceCode[posValorStart:])
                            posValorEnd = posValor2.start() + posValorStart
                            valor = sourceCode[(posValorStart + 4):posValorEnd]
                            start = end
                            df.at[index, columna + str(ver)] = valor
                        else:
                            seguir = 0
                except:
                    pass

        # Si la subasta tiene lotes
        else:
            for lote in range(1, row['lotes'] + 1):
                for ver in range(1, 7):
                    try:
                        url = "https://subastas.boe.es/detalleSubasta.php?idSub=" + codigo + "&ver=" + str(
                            ver) + "&idLote=" + str(lote)
                        sourceCode = str(request.urlopen(url).read().decode('utf-8'))
                        sourceCode = unescape(sourceCode)
                        start = 0
                        seguir = 1
                        # Recorrido del código fuente y extracción de los datos de la subasta
                        while seguir == 1:
                            match = re.search('<th>', sourceCode[start:])
                            if match:
                                m = match.start() + start
                                e = re.search('</th>', sourceCode[m:(m + 100)])
                                end = e.start() + m
                                columna = sourceCode[(m + 4):end]
                                posValor = re.search('<td>', sourceCode[end:])
                                posValorStart = posValor.start() + end
                                posValor2 = re.search('</td>', sourceCode[posValorStart:])
                                posValorEnd = posValor2.start() + posValorStart
                                valor = sourceCode[(posValorStart + 4):posValorEnd]
                                start = end

                                # Crear una nueva fila en dfLotes si es la primera iteración para este lote
                                if (row['codigo_subasta'], lote) not in dfLotes.index:
                                    data = [{'codigo_subasta': row['codigo_subasta'], 'lote': lote}]
                                    new_row = pd.DataFrame(data)
                                    dfLotes = pd.concat([dfLotes, new_row])  # No need for ignore_index=True here
                                    dfLotes.set_index(['codigo_subasta', 'lote'], inplace=True)  # Set both columns as index

                                # Asignar el valor usando .loc[], se creará la fila/columna si no existe
                                dfLotes.loc[(row['codigo_subasta'], lote), columna + str(ver)] = valor
                            else:
                                seguir = 0
                    except:
                        pass

    # Transformar los DataFrames principales
    df = transformacion(df)
    dfLotes = transformacion(dfLotes)
    dfLotes=dfLotes.reset_index(drop=True)

    # Guardar los DataFrames en archivos Excel
    df.to_excel('output\lectura_subastas.xlsx')
    dfLotes.to_excel('output\lectura_subastas_lotes.xlsx')