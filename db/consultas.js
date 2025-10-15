// 1
db.pacientes.find({
    $and: [
        { edad: { $gte: 40 } },
        {
            $or: [
                { "contacto.direccion.estado": { $in: ["CDMX", "Jalisco", "Nuevo León"] } },
                { nombre: { $regex: /^Mar/i } } // nombres que comiencen con "Mar"
            ]
        },
        { activo: true }
    ]
});

// 2
db.pacientes.find({
    historial_clinico: {
        $elemMatch: {
            fecha: { $gte: ISODate("2025-01-01") },
        }
    }
});

// 3
db.pacientes.aggregate([
    {
        $project: {
            nombre: 1,
            edad: 1,
            categoria_edad: {
                $cond: {
                    if: { $gte: ["$edad", 60] },
                    then: "Adulto mayor",
                    else: "Adulto"
                }
            },
            correo_contacto: "$contacto.email"
        }
    }
]);

// 4
db.diagnosticos.createIndex({ nombre: "text", descripcion: "text" });

db.diagnosticos.find(
    { $text: { $search: "agua" } },
    { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });

// 5
db.pacientes.createIndex({ "contacto.direccion.estado": 1, edad: -1 });

db.pacientes.find({
    "contacto.direccion.estado": "Puebla",
    edad: { $gte: 30 }
});

// 6
db.pacientes.updateOne(
    { nombre: "Juan Menchaca Vela" },
    {
        $set: { "contacto.telefono": "555-999-8888" },
        $inc: { edad: 1 },
        $push: { alergias: "polvo" },
        $pull: { condiciones_cronicas: "asma" },
        $addToSet: { dispositivos_asignados: ObjectId("68ef1589615c57bf7e3967f6") }
    }
);

// 7
db.diagnosticos.deleteMany({
    $and: [
        { activo: false },
        { fecha_creacion: { $lte: ISODate("2025-10-15") } }
    ]
});

// 8
db.tratamientos.aggregate([
    {
        $lookup: {
            from: "diagnosticos",
            localField: "diagnostico_id",
            foreignField: "_id",
            as: "diagnostico_info"
        }
    },
    { $unwind: "$diagnostico_info" },
    {
        $lookup: {
            from: "dispositivos_medicos",
            localField: "diagnostico_info.categoria",
            foreignField: "tipo",
            as: "dispositivos_relacionados"
        }
    },
    { $unwind: { path: "$dispositivos_relacionados", preserveNullAndEmptyArrays: true } },
    {
        $lookup: {
            from: "pacientes",
            localField: "dispositivos_relacionados.paciente_asignado",
            foreignField: "_id",
            as: "paciente_asignado"
        }
    },
    {
        $project: {
            _id: 0,
            tratamiento: "$nombre",
            diagnostico: "$diagnostico_info.nombre",
            categoria_diagnostico: "$diagnostico_info.categoria",
            dispositivo: "$dispositivos_relacionados.nombre",
            tipo_dispositivo: "$dispositivos_relacionados.tipo",
            paciente: { $arrayElemAt: ["$paciente_asignado.nombre", 0] },
            edad_paciente: { $arrayElemAt: ["$paciente_asignado.edad", 0] },
            en_uso: "$dispositivos_relacionados.en_uso"
        }
    }
]);


// 9
db.diagnosticos.find({
    fecha_creacion: {
        $gte: ISODate("2024-01-01T00:00:00.000Z"),
        $lte: ISODate("2025-10-15T23:59:59.999Z")
    }
});


// 10
db.pacientes.aggregate([
    { $match: { activo: true } },
    { $out: "pacientes_activos" }
]);
