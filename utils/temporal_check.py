from config.env import db

def patients_per_month():
    pipeline = [
        {"$group": {
            "_id": {
                "año": {"$year": "$fecha_registro"},
                "mes": {"$month": "$fecha_registro"}
            },
            "total": {"$sum": 1}
        }},
        {"$sort": {"_id.año": 1, "_id.mes": 1}}
    ]
    resultados = db.pacientes.aggregate(pipeline)
    lines = ["Pacientes registrados por mes:"]
    for r in resultados:
        lines.append(f"  - {r['_id']['año']}-{r['_id']['mes']:02d}: {r['total']}")
    result_str = "\n".join(lines)
    print(result_str)
    print("")
    return result_str

def patient_per_day():
    pipeline = [
        {"$group": {
            "_id": {
                "año": {"$year": "$fecha_registro"},
                "mes": {"$month": "$fecha_registro"},
                "dia": {"$dayOfMonth": "$fecha_registro"}
            },
            "total": {"$sum": 1}
        }},
        {"$sort": {"_id.año": 1, "_id.mes": 1, "_id.dia": 1}}
    ]
    resultados = db.pacientes.aggregate(pipeline)
    lines = ["Pacientes registrados por día:"]
    for r in resultados:
        lines.append(f"  - {r['_id']['año']}-{r['_id']['mes']:02d}-{r['_id']['dia']:02d}: {r['total']}")
    result_str = "\n".join(lines)
    print(result_str)
    print("")
    return result_str

def patient_per_year():
    pipeline = [
        {"$group": {
            "_id": {"año": {"$year": "$fecha_registro"}},
            "total": {"$sum": 1}
        }},
        {"$sort": {"_id.año": 1}}
    ]
    resultados = db.pacientes.aggregate(pipeline)
    lines = ["Pacientes registrados por año:"]
    for r in resultados:
        lines.append(f"  - {r['_id']['año']}: {r['total']}")
    result_str = "\n".join(lines)
    print(result_str)
    print("")
    return result_str

def first_and_last_field():
    primero = db.pacientes.find_one(sort=[("fecha_registro", 1)])
    ultimo = db.pacientes.find_one(sort=[("fecha_registro", -1)])
    lines = ["Primer registro de paciente:"]
    if primero:
        lines.append(f"  - {primero['fecha_registro']}")
    lines.append("Último registro de paciente:")
    if ultimo:
        lines.append(f"  - {ultimo['fecha_registro']}")
    result_str = "\n".join(lines)
    print(result_str)
    print("")
    return result_str

def check_all(export_file="documents/results.txt"):
    results = []
    results.append(patients_per_month())
    results.append(patient_per_year())
    results.append(first_and_last_field())
    # results.append(patient_per_day())
    with open(export_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))
    print(f"Resultados exportados a {export_file}")