from config.db import init_db
from config.create_db import create_collections
from seed.data_generator import seed_all
from utils.indexes import check_changes_indexes
from utils.anomalous_check import detect_anomalous
from utils.temporal_check import check_all
from utils.export_data import export_all

if __name__ == "__main__":
    print("=== Inicialización de la base de datos y creación de colecciones ===")
    create_collections()
    print("")
    init_db()
    print("")
    print("=== Carga de los datos ===")
    seed_all()    
    print("")
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
