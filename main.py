from config.db import init_db
from config.create_db import create_collections
from seed.data_generator import seed_all
from utils.indexes import check_changes_indexes
from utils.anomalous_check import detect_anomalous
from utils.temporal_check import check_all
from utils.export_data import export_all
from utils.execute_js import execute_js_file

if __name__ == "__main__":
    print("------ PARTE 1 ------")
    print("=== Inicialización de la base de datos y creación de colecciones ===")
    create_collections()
    print("")
    init_db()
    print("")
    print("------ PARTE 2 ------")
    print("=== Carga de los datos ===")
    seed_all()    
    print("")
    print("------ PARTE 3 ------")
    print("=== Ejecución de consultas ===")
    execute_js_file("db/consultas.js")
    print("")
    print("------ PARTE 4 ------")
    print("=== Ejecución de pipelines de relacion ===")
    execute_js_file("db/pipelines.js")
    print("")
    print("------ PARTE 5 ------")
    print("=== Verificación de índices y planes de consulta ===")
    check_changes_indexes()
    print("")
    print("=== Detección de anomalías en los datos ===")
    detect_anomalous()
    print("")
    print("=== Verificación de consistencia temporal ===")
    check_all()
    print("")
    print("=== Exportación de datos ===")
    export_all()
