# Importamos las librerías necesarias
from pathlib import Path  # Para gestionar los directorios
import os  # Para obtener la lista de archivos
import csv  # Para trabajar con los archivos csv

MyFolder = Path.cwd()  # El directorio donde guardamos los archivos
MyFiles = os.listdir(MyFolder)  # La lista de archivos en el directorio

MyCSVFiles = []  # La lista vacía para añadirle archivos .csv en el bucle

files = 0  # Contador de archivos de tipo .csv
i = 0  # Contador de líneas pegadas
errors = 0  # Contador de errores detectados al pegar

for file in MyFiles:  # Por cada uno de los archivos de la carpeta
    if file.endswith(".csv"):  # Si la extensión es .csv
        files += 1
        MyCSVFiles.append(file)  # Lo añadimos a la lista que hemos creado antes
if files == 0:
    print("No hay archivos .csv en la carpeta")
    exit()  # Salimos del programa, no hay nada que convertir

# Una vez que hemos comprobado que hay archivos .csv, creamos el archivo para unificar los datos
write_to = open(MyFolder / 'paste.csv', 'w', newline='',
                encoding="utf8")  # Creamos un archivo csv nuevo para pegar los datos
# OJO! Importante indicar el encoding="utf-8". Si no, usará el encoding 1252, que da problemas con caracteres no latinos
writer = csv.writer(write_to)  # Creamos un objeto writer para escribir sobre nuestro nuevo archivo

# Creamos, si no existe, una carpeta de backup para mover los archivos que vamos a copiar
if not (MyFolder / 'backup').exists():
    os.makedirs(MyFolder / 'backup')
    print("Creado el directorio de respaldo")
else:
    print("El directorio de respaldo ya existe")

for file in MyCSVFiles:  # bucle por todos los archivos csv
    j = 0  # Contador de filas en cada archivo
    currentFile = open(MyFolder / file, encoding="utf8")  # Abrimos el archivo
    currentReader = csv.reader(currentFile)  # Creamos un objeto reader para leer del archivo
    currentData = list(currentReader)  # Convertimos el archivo en una lista por cada fila
    print("Procesando el archivo " + file)
    if file == MyCSVFiles[0]:  # Cogemos los encabezados del primer archivo, pero solamente una vez
        writer.writerow(currentData[0])  # Pegamos la primera fila del primer archivo
    for row in currentData[1:]:  # Nos saltamos la primera fila (índice 0) porque son los nombres de columna
        try:
            writer.writerow(row)  # Escribimos al archivo de destino
        except Exception:
            print("No se ha podido escribir la línea " + str(j) + "en el archivo " +
                  file + "debido a errores")  # Salvo que haya un error al pegar
            errors += 1  # Apuntamos los errores que llevamos
        i += 1
        j += 1
    print("Se han copiado con éxito " + str(j) + " filas en el archivo " + file)
    currentFile.close()  # Si no cerramos el archivo, no lo podremos mover a la carpeta de backup
    if 'all.csv' in file:  # All.csv existirá si ya se ha usado el programa antes
        os.remove(MyFolder / file)  # Ya tenemos backup de todo lo que hay en all, es redundante
        print("El archivo " + file + " ha sido eliminado con éxito")
    else:
        os.rename(MyFolder / file, MyFolder / 'backup' / file)
        print("Se ha movido con éxito el archivo " + file)
print("Se han pegado con éxito " + str(i) + " filas")
print("No se han podido pegar " + str(errors) + " filas debido a errores")
write_to.close()  # Cerramos el archivo para poderlo renombrar

# A continuación, renombramos "paste.csv" como "all.csv"
for file in os.listdir(MyFolder):  # La lista de archivos en el directorio
    if "paste.csv" in file:
        os.rename(MyFolder / file, MyFolder / "all.csv")
        print("El archivo " + file + " ha sido renombrado con éxito a all.csv")
