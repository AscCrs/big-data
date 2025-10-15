import subprocess
from config.env import client, db_name

def execute_js_file(js_path, db_name=db_name, mongo_uri=client):
    """
    Ejecuta un archivo .js de MongoDB usando el shell desde Python.
    """
    comando = [
        "mongosh",
        db_name,
        js_path,
        "--quiet",
        "--host", "localhost"
    ]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print(f"Salida de {js_path}:\n{resultado.stdout}")
        if resultado.stderr:
            print(f"Errores:\n{resultado.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {js_path}: {e.stderr}")
