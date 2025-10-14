from faker import Faker
import random
from models.paciente import Paciente, Contacto, Direccion, HistorialClinico
from models.doctor import Doctor, Horarios, Ubicacion
from models.diagnostico import Diagnostico
from models.tratamiento import Tratamiento, Paso
from models.dispositivo_medico import DispositivoMedico, Mantenimiento

fake = Faker("es_MX")

def null_generator(value):
    """Devuelve None aleatoriamente para simular datos faltantes"""
    return value if random.random() > 0.2 else None

def seed_diagnosticos(n=200):
    Diagnostico.objects.delete()
    for _ in range(n):
        Diagnostico(
            codigo=fake.bothify(text="DX-###"),
            nombre=fake.word(),
            descripcion=null_generator(fake.text()),
            categoria=null_generator(random.choice(["cardiologia", "neurologia", "oncologia"])),
            activo=random.choice([True, False])
        ).save()

def seed_tratamientos(n=200):
    Tratamiento.objects.delete()
    diagnosticos = list(Diagnostico.objects)
    for _ in range(n):
        t = Tratamiento(
            nombre=fake.catch_phrase(),
            diagnostico_id=random.choice(diagnosticos) if diagnosticos else None,
            pasos=[Paso(etapa=i, descripcion=fake.sentence()) for i in range(random.randint(1, 3))],
            medicamentos=[fake.word() for _ in range(random.randint(0, 3))],
            duracion_estimada_dias=random.randint(5, 60),
            requiere_hospitalizacion=random.choice([True, False]),
            observaciones=null_generator(fake.sentence())
        )
        t.save()

def seed_doctores(n=200):
    Doctor.objects.delete()
    for _ in range(n):
        Doctor(
            nombre=fake.name(),
            especialidad=random.choice(["Pediatría", "Cardiología", "Oncología", "Neurología"]),
            licencia_medica=fake.bothify(text="LIC-#####"),
            fecha_contratacion=fake.date_time_between(start_date="-10y", end_date="now"),
            activo=random.choice([True, False]),
            horarios=Horarios(
                lunes=null_generator([f"{h}:00" for h in range(8, 13)]),
                martes=null_generator([f"{h}:00" for h in range(8, 13)]),
            ),
            ubicacion=Ubicacion(
                hospital=fake.company(),
                sala=null_generator(fake.bothify(text="Sala ##"))
            )
        ).save()

def seed_dispositivos(n=200):
    DispositivoMedico.objects.delete()
    for _ in range(n):
        DispositivoMedico(
            nombre=fake.word(),
            tipo=random.choice(["Monitor", "Bomba", "Sensor", "Respirador"]),
            fabricante=null_generator(fake.company()),
            en_uso=random.choice([True, False]),
            mantenimiento=[
                Mantenimiento(fecha=fake.date_time_between(start_date="-1y", end_date="now"),
                              descripcion=null_generator(fake.sentence()))
                for _ in range(random.randint(0, 2))
            ]
        ).save()

def seed_pacientes(n=200):
    Paciente.objects.delete()
    doctores = list(Doctor.objects)
    dispositivos = list(DispositivoMedico.objects)
    tratamientos = list(Tratamiento.objects)
    diagnosticos = list(Diagnostico.objects)

    for _ in range(n):
        Paciente(
            nombre=fake.name(),
            edad=random.randint(1, 99),
            sexo=random.choice(["M", "F", "Otro"]),
            contacto=Contacto(
                telefono=null_generator(fake.phone_number()),
                email=null_generator(fake.email()),
                direccion=Direccion(
                    calle=null_generator(fake.street_name()),
                    ciudad=null_generator(fake.city()),
                    estado=null_generator(fake.state()),
                    cp=null_generator(fake.postcode())
                )
            ),
            activo=random.choice([True, False]),
            alergias=random.choice([["penicilina", "mariscos", "latex", "benzocaina", "lana"], [], None]),
            condiciones_cronicas=random.choice([["diabetes", "hipertensión", "asma", "arritmias"], [], None]),
            historial_clinico=[
                HistorialClinico(
                    fecha=fake.date_time_between(start_date="-2y", end_date="now"),
                    diagnostico_id=random.choice(diagnosticos) if diagnosticos else None,
                    tratamiento_id=random.choice(tratamientos) if tratamientos else None,
                    doctor_id=random.choice(doctores) if doctores else None,
                    notas=null_generator(fake.sentence())
                ) for _ in range(random.randint(0, 3))
            ],
            dispositivos_asignados=random.sample(dispositivos, k=min(len(dispositivos), random.randint(0, 2)))
        ).save()

def seed_all():
    print("=== Carga de los datos ===")
    seed_diagnosticos()
    seed_tratamientos()
    seed_doctores()
    seed_dispositivos()
    seed_pacientes()
    print("Datos cargados correctamente.")
