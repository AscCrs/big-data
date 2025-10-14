from mongoengine import connect

def init_db():
    connect(
        db="gestion_hospitalaria",
        host="mongodb://localhost:27017/gestion_hospitalaria",
        alias="default"
    )
