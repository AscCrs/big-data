from pymongo import MongoClient

# Conexión 
client = MongoClient("mongodb://localhost:27017/")
db_name = "gestion_hospitalaria"
db = client[db_name]

print(f"Base de datos creada o conectada: {db_name}\n")

# Colecciones y validadores
collections = {
    "pacientes": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["nombre", "edad", "sexo"],
            "properties": {
                "nombre": {"bsonType": "string"},
                "edad": {"bsonType": "int"},
                "sexo": {"enum": ["M", "F", "Otro"]},
                "contacto": {
                    "bsonType": "object",
                    "properties": {
                        "telefono": {"bsonType": "string"},
                        "email": {"bsonType": "string"},
                        "direccion": {
                            "bsonType": "object",
                            "properties": {
                                "calle": {"bsonType": "string"},
                                "ciudad": {"bsonType": "string"},
                                "estado": {"bsonType": "string"},
                                "cp": {"bsonType": "string"},
                            },
                        },
                    },
                },
                "fecha_registro": {"bsonType": "date"},
                "activo": {"bsonType": "bool"},
                "alergias": {"bsonType": "array", "items": {"bsonType": "string"}},
                "condiciones_cronicas": {"bsonType": "array", "items": {"bsonType": "string"}},
                "historial_clinico": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "fecha": {"bsonType": "date"},
                            "diagnostico_id": {"bsonType": "objectId"},
                            "tratamiento_id": {"bsonType": "objectId"},
                            "doctor_id": {"bsonType": "objectId"},
                            "notas": {"bsonType": "string"}
                        },
                    },
                },
                "dispositivos_asignados": {
                    "bsonType": "array",
                    "items": {"bsonType": "objectId"}
                },
            },
        }
    },
    "doctores": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["nombre", "especialidad", "licencia_medica"],
            "properties": {
                "nombre": {"bsonType": "string"},
                "especialidad": {"bsonType": "string"},
                "licencia_medica": {"bsonType": "string"},
                "fecha_contratacion": {"bsonType": "date"},
                "activo": {"bsonType": "bool"},
                "pacientes_asignados": {"bsonType": "array", "items": {"bsonType": "objectId"}},
                "horarios": {
                    "bsonType": "object",
                    "properties": {
                        "lunes": {"bsonType": "array", "items": {"bsonType": "string"}},
                        "martes": {"bsonType": "array", "items": {"bsonType": "string"}},
                        "miercoles": {"bsonType": "array", "items": {"bsonType": "string"}},
                        "jueves": {"bsonType": "array", "items": {"bsonType": "string"}},
                        "viernes": {"bsonType": "array", "items": {"bsonType": "string"}},
                    },
                },
                "ubicacion": {
                    "bsonType": "object",
                    "properties": {
                        "hospital": {"bsonType": "string"},
                        "sala": {"bsonType": "string"},
                    },
                },
            },
        }
    },
    "diagnosticos": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["codigo", "nombre"],
            "properties": {
                "codigo": {"bsonType": "string"},
                "nombre": {"bsonType": "string"},
                "descripcion": {"bsonType": "string"},
                "categoria": {"bsonType": "string"},
                "fecha_creacion": {"bsonType": "date"},
                "activo": {"bsonType": "bool"}
            },
        }
    },
    "tratamientos": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["nombre"],
            "properties": {
                "nombre": {"bsonType": "string"},
                "diagnostico_id": {"bsonType": "objectId"},
                "pasos": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "etapa": {"bsonType": "int"},
                            "descripcion": {"bsonType": "string"},
                        },
                    },
                },
                "medicamentos": {"bsonType": "array", "items": {"bsonType": "string"}},
                "duracion_estimada_dias": {"bsonType": "int"},
                "requiere_hospitalizacion": {"bsonType": "bool"},
                "observaciones": {"bsonType": "string"},
            },
        }
    },
    "dispositivos_medicos": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["nombre", "tipo"],
            "properties": {
                "nombre": {"bsonType": "string"},
                "tipo": {"bsonType": "string"},
                "fabricante": {"bsonType": "string"},
                "fecha_adquisicion": {"bsonType": "date"},
                "en_uso": {"bsonType": "bool"},
                "paciente_asignado": {"bsonType": "objectId"},
                "mantenimiento": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "fecha": {"bsonType": "date"},
                            "descripcion": {"bsonType": "string"},
                        },
                    },
                },
            },
        }
    },
}

def create_collections():
    # Validaciones y creacion de las colecciones
    for name, validator in collections.items():
        if name in db.list_collection_names():
            print(f"Colección existente: {name}")
            db.command({
                "collMod": name,
                "validator": validator,
                "validationLevel": "strict"
            })
        else:
            db.create_collection(name, validator=validator)
            print(f"Colección creada: {name}")

    print("\Estructura terminada.")