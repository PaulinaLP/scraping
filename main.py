import datetime
import time
from scraping_subastas import scrape_subastas
from scraping_subastas_lectura import lectura
def main():
    # Registrar tiempo de inicio
    started_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    # Definir los enlaces de las subastas
    my_dic = {'finalizada': "https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_U1JQSFQzQ0dKT3dvQkZib0hpdEZpaWZrdVB5bmVjcks3M0FLY3MzTWVpclJwNTFQVGlvOUNoN3lFUUYyek1STVlDK1J4UG5Ha2trbHBVeGV6RFpSWWR5Z0ZBZUxxMTlNcGpFQ2dXMWlXbTRNUEZaYktMWitwNDVCdGgrQlpKSzV6Mk1qQWMxUkUzdEZXVGdjTmNYRWs0MDNhTXJpUTk4WEU5SXlBWWxBTDE3NU9hT1JUbmEvWnBITjM2YTJMbzB2R2szVFlQcVg2cUJtd0RVcVNmWk44b2d3L2hmM0gxUUJ0VXpkZS9rQXpSSlVKZndhMU1jRzU0NnZ2Y0pzNHE2Yg,,-",
              'concluida': "https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_Zk1jcVFGRnV4Z3dTS0RPSVE2cXRQL2l6RTJaaFVuSE10SG1LMWYxTjB5M2hEQWdMYndhVEt1VHhsYmwrMHo3N3lOYVk2Sjk2ditRVHdqUnpqRElhYmNXR0JCS3luTExydm9oWDRMa0U5M01Xc0FUc29uNmx2ZExiTnpNY0tOdk9vRkg0UnY2YkdsVGZRVFZSSWwzNG1mNHQxYmlsZjN1UU1OTHlLNnhvRVVkL0FCT01tdDIvTVVHR3B3K29QNWJLYXBiK0pndWZxSDZKZDBaSHVaZWFhc3czQlJjTHl4d2REZ2djWWZ4M05Bby9iaHNPL3dyK09NTVpKeTZUR2E2Tg,,-"}
    # Obtener datos de subastas
    my_df = scrape_subastas(my_dic)
    # Guardar datos en un archivo Excel
    my_df.to_excel("output/output.xlsx", index=False)
    lectura()

if __name__ == "__main__":
    main()