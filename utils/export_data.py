import os
import json
from models.paciente import Paciente
from models.doctor import Doctor
from models.diagnostico import Diagnostico
from models.tratamiento import Tratamiento
from models.dispositivo_medico import DispositivoMedico
from config.db import init_db

collections = {
    "pacientes": Paciente,
    "doctores": Doctor,
    "diagnosticos": Diagnostico,
    "tratamientos": Tratamiento,
    "dispositivos_medicos": DispositivoMedico,
}

def export_all_collections(output_dir="documents"):
    """
    Exporta todas las colecciones a archivos JSON individuales.
    """
    init_db()  # conexión
    os.makedirs(output_dir, exist_ok=True)

    for name, model in collections.items():
        data = []
        for doc in model.objects:
            # Se serializa el documento en un diccionario
            doc_dict = json.loads(doc.to_json())
            data.append(doc_dict)

        file_path = os.path.join(output_dir, f"{name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Se exportaron {len(data)} documentos de '{name}' -> {file_path}")

    print("\Almacenamiento completo.")

def export_all_data(output_dir="documents"):
    """
    Exporta todas las colecciones en un solo JSON.
    """
    all_data = {}
    for name, model in collections.items():
        all_data[name] = [json.loads(doc.to_json()) for doc in model.objects]

    file_path = os.path.join(output_dir, "backup_total.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"Se exportaron todas las colecciones a {file_path}")



if __name__ == "__main__":
    export_all_collections()
    export_all_data()
