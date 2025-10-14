from mongoengine import Document, StringField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ListField, ReferenceField
import datetime

class Mantenimiento(EmbeddedDocument):
    fecha = DateTimeField(default=datetime.datetime.utcnow)
    descripcion = StringField()

class DispositivoMedico(Document):
    nombre = StringField(required=True)
    tipo = StringField(required=True)
    fabricante = StringField()
    fecha_adquisicion = DateTimeField(default=datetime.datetime.utcnow)
    en_uso = BooleanField(default=False)
    paciente_asignado = ReferenceField("Paciente")
    mantenimiento = ListField(EmbeddedDocumentField(Mantenimiento))

    meta = {"collection": "dispositivos_medicos"}
