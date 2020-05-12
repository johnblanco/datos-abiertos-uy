# Creación de Empresas a través de Empresa en el Dia 

Estudio de los datos [provistos por Agesic](https://catalogodatos.gub.uy/dataset/agesic-creacion-de-empresas-a-traves-de-empresa-en-el-dia)

Utiliza [dash](https://plotly.com/dash/) para visualizar los datos

## Calidad de los datos

* Los nombres de archivo no siguen un patrón estándar: Algunos empiezan con un prefijo con la fecha (ej 092018_datos-abiertos-montevideo.csv) pero la mitad de los archivos no cuentan con este.
* El archivo diciembre-2019.csv y el archivo noviembre-2019.csv no queda claro de que departamento son, asumo que son de Montevideo.
* Las columnas de los csvs no son consistentes, algunos tienen las columnas: RUT,Razón Social,Tipo y otros vienen con Nombre de la sociedad,Nombre del proceso,Número de RUT,Número de BPS 
* Supongo que hay tipos de empresa que representan lo mismo como MS/MONO MIDES?, UNIPERSONALES/UNIPERSONAL, SOCIEDAD AN?NIMA/SA

## Descripción de los scripts


### app.py

Es la app dash, ahi se define el layout y los callbacks, todo en python.

### download_csvs.py

Parsea el xml y descarga los 73 csvs en la carpeta /csvs

### parse_data.py

Arma un dataframe único con los datos de los csvs anteriores.

