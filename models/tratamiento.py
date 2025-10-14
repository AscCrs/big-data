from mongoengine import Document, StringField, BooleanField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField

class Paso(EmbeddedDocument):
    etapa = IntField()
    descripcion = StringField()

class Tratamiento(Document):
    nombre = StringField(required=True)
    diagnostico_id = ReferenceField("Diagnostico")
    pasos = ListField(EmbeddedDocumentField(Paso))
    medicamentos = ListField(StringField())
    duracion_estimada_dias = IntField()
    requiere_hospitalizacion = BooleanField(default=False)
    observaciones = StringField()

    meta = {"collection": "tratamientos"}
