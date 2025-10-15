import json
from datetime import datetime
from config.env import db

def detectar_anomalias_pacientes():
    anomalías = []
    for p in db.pacientes.find({"$or": [{"edad": {"$lt": 0}}, {"edad": {"$gt": 120}}]}):
        anomalías.append({"tipo": "edad_anomala", "nombre": p.get("nombre"), "edad": p.get("edad")})
    hoy = datetime.now()
    for p in db.pacientes.find({"fecha_registro": {"$gt": hoy}}):
        anomalías.append({"tipo": "fecha_registro_futura", "nombre": p.get("nombre"), "fecha_registro": str(p.get("fecha_registro"))})
    campos_obligatorios = ["edad", "alergias", "condiciones_cronicas"]
    for campo in campos_obligatorios:
        for p in db.pacientes.find({campo: {"$exists": False}}):
            anomalías.append({"tipo": "campo_faltante", "campo": campo, "_id": str(p.get("_id"))})
    return anomalías

def detectar_anomalias_medicos():
    anomalías = []
    for m in db.medicos.find({"$or": [{"edad": {"$lt": 18}}, {"edad": {"$gt": 100}}]}):
        anomalías.append({"tipo": "edad_anomala", "nombre": m.get("nombre"), "edad": m.get("edad")})
    for m in db.medicos.find({"especialidad": {"$exists": False}}):
        anomalías.append({"tipo": "campo_faltante", "campo": "especialidad", "_id": str(m.get("_id"))})
    hoy = datetime.now()
    for m in db.medicos.find({"fecha_contratacion": {"$gt": hoy}}):
        anomalías.append({"tipo": "fecha_contratacion_futura", "nombre": m.get("nombre"), "fecha_contratacion": str(m.get("fecha_contratacion"))})
    return anomalías

def detectar_anomalias_citas():
    anomalías = []
    hoy = datetime.now()
    for c in db.citas.find({"fecha": {"$lt": hoy}}):
        anomalías.append({"tipo": "cita_pasada", "_id": str(c.get("_id")), "fecha": str(c.get("fecha"))})
    for c in db.citas.find():
        if not db.pacientes.find_one({"_id": c.get("paciente_id")}):
            anomalías.append({"tipo": "paciente_inexistente", "_id": str(c.get("_id"))})
        if not db.medicos.find_one({"_id": c.get("medico_id")}):
            anomalías.append({"tipo": "medico_inexistente", "_id": str(c.get("_id"))})
    campos_obligatorios = ["paciente_id", "medico_id", "fecha"]
    for campo in campos_obligatorios:
        for c in db.citas.find({campo: {"$exists": False}}):
            anomalías.append({"tipo": "campo_faltante", "campo": campo, "_id": str(c.get("_id"))})
    return anomalías

def detectar_anomalias_recetas():
    anomalías = []
    hoy = datetime.now()
    for r in db.recetas.find({"fecha_emision": {"$gt": hoy}}):
        anomalías.append({"tipo": "fecha_emision_futura", "_id": str(r.get("_id")), "fecha_emision": str(r.get("fecha_emision"))})
    for r in db.recetas.find():
        if not db.pacientes.find_one({"_id": r.get("paciente_id")}):
            anomalías.append({"tipo": "paciente_inexistente", "_id": str(r.get("_id"))})
        if not db.medicos.find_one({"_id": r.get("medico_id")}):
            anomalías.append({"tipo": "medico_inexistente", "_id": str(r.get("_id"))})
    for r in db.recetas.find({"$or": [{"medicamentos": {"$exists": False}}, {"medicamentos": {"$size": 0}}]}):
        anomalías.append({"tipo": "medicamentos_faltantes", "_id": str(r.get("_id"))})
    return anomalías

def exportar_anomalias_json(path="documents/anomalias.json"):
    datos = {
        "pacientes": detectar_anomalias_pacientes(),
        "medicos": detectar_anomalias_medicos(),
        "citas": detectar_anomalias_citas(),
        "recetas": detectar_anomalias_recetas(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Anomalías exportadas a {path}")

def detect_anomalous():
    # Si solo quieres imprimir:
    for tipo, lista in [
        ("pacientes", detectar_anomalias_pacientes()),
        ("medicos", detectar_anomalias_medicos()),
        ("citas", detectar_anomalias_citas()),
        ("recetas", detectar_anomalias_recetas()),
    ]:
        print(f"Anomalías en {tipo}:")
        for a in lista:
            print(f"  - {a}")
        print("")
    
    # Si quieres exportar:
    exportar_anomalias_json()
