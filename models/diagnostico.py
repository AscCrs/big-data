from mongoengine import Document, StringField, DateTimeField, BooleanField
import datetime

class Diagnostico(Document):
    codigo = StringField(required=True)
    nombre = StringField(required=True)
    descripcion = StringField()
    categoria = StringField()
    fecha_creacion = DateTimeField(default=datetime.datetime.utcnow)
    activo = BooleanField(default=True)

    meta = {"collection": "diagnosticos"}
