from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField
import datetime

class Horarios(EmbeddedDocument):
    lunes = ListField(StringField())
    martes = ListField(StringField())
    miercoles = ListField(StringField())
    jueves = ListField(StringField())
    viernes = ListField(StringField())

class Ubicacion(EmbeddedDocument):
    hospital = StringField()
    sala = StringField()

class Doctor(Document):
    nombre = StringField(required=True)
    especialidad = StringField(required=True)
    licencia_medica = StringField(required=True)
    fecha_contratacion = DateTimeField(default=datetime.datetime.utcnow)
    activo = BooleanField(default=True)
    pacientes_asignados = ListField(ReferenceField("Paciente"))
    horarios = EmbeddedDocumentField(Horarios)
    ubicacion = EmbeddedDocumentField(Ubicacion)

    meta = {"collection": "doctores"}
