import os
import pandas as pd

def listar_directorio_en_excel(directorio, nombre_excel="estructura_directorio.xlsx"):
    datos = []

    for ruta, subdirs, archivos in os.walk(directorio):
        # Agregar carpetas
        for subdir in subdirs:
            datos.append([os.path.join(ruta, subdir), ruta, subdir, "Carpeta", ""])

        # Agregar archivos
        for archivo in archivos:
            ruta_completa = os.path.join(ruta, archivo)
            tamaño = os.path.getsize(ruta_completa)  # Tamaño en bytes
            datos.append([ruta_completa, ruta, archivo, "Archivo", tamaño])

    # Convertir a DataFrame
    df = pd.DataFrame(datos, columns=["Ruta Completa", "Carpeta Padre", "Nombre", "Tipo", "Tamaño (bytes)"])

    # Guardar en un archivo Excel
    df.to_excel(nombre_excel, index=False)
    print(f"Archivo Excel guardado como: {nombre_excel}")

# 📂 Cambia esta ruta al directorio que deseas listar
directorio_a_listar = "G:\Mi unidad\Freelance\Intra-embrace"

listar_directorio_en_excel(directorio_a_listar)
