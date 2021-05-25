
App para escanear base de datos MySql con persistencia de los resultados de los escaneos en MongoDB.

La base de datos mongodb, que accede a tres documentos diferentes dentro de "databases_scan"

  - connections: donde almacena los datos de conexiones enviadas

  - scans: donde se almacena el objeto final construido con el resultado de un escaneo

  -sequences: creado especificamente para tener un valor que simule un contador autoincremental

Observaciones:

    Los datos se obtiene ordenados, en este formato: (TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME). La query enviada a la base de datos es la que sigue:

    El formato final es un json, que distingue columnas por tabla, y a su vez por schema con la estructura del archivo adjunto "scan_example.json"

  - Para dar la versatilidad de cambiar los tipos a clasificar en los nombres de las columnas, la api lee un archivo donde se deben cargar los mismos.
    El mismo ubicado en: "python_flask_app\app\utils\information_type.txt"

  - Se adjuntan los script para creacion de dos schemas en MySQL obtenidos desde su pagina oficial.



Instrucciones:

  - activar entorno virtual venv: "venv\Scripts\activate.bat"

  - base mongodb ejecutandose acorde al enlace de conexion: "mongodb://localhost:5000/databases_scan"

  - base MySQL ejecutandose

  - ejecutar archivo "runner.py" para iniciar el servidor

  - importar la postman collection adjunta para ver los escaneos
