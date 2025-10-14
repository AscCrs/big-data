from mongoengine import (
    Document, StringField, IntField, BooleanField, DateTimeField,
    EmbeddedDocument, EmbeddedDocumentField, ListField, ReferenceField
)
import datetime


class Direccion(EmbeddedDocument):
    calle = StringField()
    ciudad = StringField()
    estado = StringField()
    cp = StringField()


class Contacto(EmbeddedDocument):
    telefono = StringField()
    email = StringField()
    direccion = EmbeddedDocumentField(Direccion)


class HistorialClinico(EmbeddedDocument):
    fecha = DateTimeField(default=datetime.datetime.utcnow)
    diagnostico_id = ReferenceField("Diagnostico")
    tratamiento_id = ReferenceField("Tratamiento")
    doctor_id = ReferenceField("Doctor")
    notas = StringField()


class Paciente(Document):
    nombre = StringField(required=True)
    edad = IntField(required=True)
    sexo = StringField(choices=["M", "F", "Otro"])
    contacto = EmbeddedDocumentField(Contacto)
    fecha_registro = DateTimeField(default=datetime.datetime.utcnow)
    activo = BooleanField(default=True)
    alergias = ListField(StringField())
    condiciones_cronicas = ListField(StringField())
    historial_clinico = ListField(EmbeddedDocumentField(HistorialClinico))
    dispositivos_asignados = ListField(ReferenceField("DispositivoMedico"))

    meta = {"collection": "pacientes"}
