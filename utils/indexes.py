from config.env import db
import pprint

# Creacion de indices especializados
# Campos clave para aceleracoin de consultas posiblemente 
# frecuentes y analisis: fecha_registro de pacientes,
# fecha_contratacion de doctores y campos de fechas en 
# historiales y mantenimientos.
# Índices compuestos para búsquedas por múltiples criterios.
def create_indexes():
    print("Creacion de indices")
    db.pacientes.create_index("fecha_registro")
    db.doctores.create_index("fecha_contratacion")
    db.diagnosticos.create_index("fecha_creacion")
    db.dispositivos_medicos.create_index("fecha_adquisicion")
    db.pacientes.create_index([("nombre", 1), ("fecha_registro", -1)])
    print("Índices creados.")


def show_indexes():
    colecciones = ["pacientes", "doctores", "diagnosticos", "dispositivos_medicos"]
    for col in colecciones:
        print(f"\nÍndices en '{col}':")
        for idx in db[col].list_indexes():
            print(f"  - Nombre: {idx.get('name')}")
            print(f"    Campos: {idx.get('key')}")
            print(f"    Único: {idx.get('unique', False)}")
            print(f"    Tipo: {idx.get('type', 'regular')}")
            print("")

def explain_query(collection, query):
    print(f"Plan de ejecución para {collection}:")
    plan = db[collection].find(query).explain()
    print(plan)

def check_changes_indexes():
    print("Índices antes de crear")
    show_indexes()
    print("Plan de consulta antes de índices")
    plan = db["pacientes"].find({"fecha_registro": {"$gte": "2023-01-01"}}).explain()
    pprint.pprint(plan)

    create_indexes()

    print("Índices después de crear")
    show_indexes()
    print("Plan de consulta después de índices")
    plan = db["pacientes"].find({"fecha_registro": {"$gte": "2023-01-01"}}).explain()
    pprint.pprint(plan)