// Analisis de comportamiento
db.pacientes.aggregate([
    { $unwind: "$historial_clinico" },
    {
        $lookup: {
            from: "diagnosticos",
            localField: "historial_clinico.diagnostico_id",
            foreignField: "_id",
            as: "diag"
        }
    },
    {
        $facet: {
            eventos_por_mes: [
                {
                    $group: {
                        _id: {
                            year: { $year: "$historial_clinico.fecha" },
                            month: { $month: "$historial_clinico.fecha" }
                        },
                        totalEventos: { $sum: 1 }
                    }
                },
                { $sort: { "_id.year": 1, "_id.month": 1 } }
            ],
            top_diagnosticos: [
                {
                    $group: {
                        _id: { nombre: { $arrayElemAt: ["$diag.nombre", 0] } },
                        casos: { $sum: 1 }
                    }
                },
                { $sort: { casos: -1 } },
                { $limit: 10 }
            ],
            pacientes_mas_activos: [
                {
                    $group: {
                        _id: "$_id",
                        nombre: { $first: "$nombre" },
                        eventos: { $sum: 1 }
                    }
                },
                { $sort: { eventos: -1 } },
                { $limit: 10 }
            ]
        }
    }
]);

// Metricas
db.pacientes.aggregate([
    { $unwind: "$historial_clinico" },
    {
        $lookup: {
            from: "diagnosticos",
            localField: "historial_clinico.diagnostico_id",
            foreignField: "_id",
            as: "diag"
        }
    },
    {
        $group: {
            _id: { $arrayElemAt: ["$diag.nombre", 0] }, // nombre 
            total_casos: { $sum: 1 },                   // cuenta 
            pacientes_unicos: { $addToSet: "$_id" },    // set 
            avg_edad: { $avg: "$edad" }                 // promedio de edad 
        }
    },
    {
        $project: {
            diagnostico: "$_id",
            total_casos: 1,
            total_pacientes: { $size: "$pacientes_unicos" },
            avg_edad: { $round: ["$avg_edad", 1] }
        }
    },
    { $sort: { total_casos: -1 } }
]);

// Procesamiento de arreglos anidados
db.pacientes.aggregate([
    { $unwind: "$alergias" }
]);

// Clasificacion por categorias dinamicas
db.pacientes.aggregate([
    {
        $bucket: {
            groupBy: "$edad",
            boundaries: [0, 18, 30, 45, 60, 80, 120],
            default: "Otro",
            output: {
                totalPacientes: { $sum: 1 },
                promedioEdad: { $avg: "$edad" },
                listaPacientes: { $push: { id: "$_id", nombre: "$nombre" } }
            }
        }
    },
    { $sort: { totalPacientes: -1 } }
])

// Condicionales logicos complejos
db.pacientes.aggregate([
    {
        $project: {
            nombre: 1,
            edad: 1,
            condiciones_cronicas: 1,
            alergias: 1,
            n_condiciones: { $size: { $ifNull: ["$condiciones_cronicas", []] } },
            n_alergias: { $size: { $ifNull: ["$alergias", []] } },
            riesgo: {
                $switch: {
                    branches: [
                        { case: { $or: [{ $gte: ["$edad", 75] }, { $gte: [{ $size: { $ifNull: ["$condiciones_cronicas", []] } }, 3] }] }, then: "Alto" },
                        { case: { $or: [{ $and: [{ $gte: ["$edad", 60] }, { $lt: ["$edad", 75] }] }, { $and: [{ $gte: [{ $size: { $ifNull: ["$condiciones_cronicas", []] } }, 1] }, { $lte: [{ $size: { $ifNull: ["$condiciones_cronicas", []] } }, 2] }] }] }, then: "Moderado" },
                        { case: { $gte: [{ $size: { $ifNull: ["$alergias", []] } }, 2] }, then: "Moderado" }
                    ],
                    default: "Bajo"
                }
            }
        }
    }
]);

// Integracion de colecciones
db.pacientes.aggregate([
    { $unwind: "$historial_clinico" },
    {
        $lookup: {
            from: "diagnosticos",
            localField: "historial_clinico.diagnostico_id",
            foreignField: "_id",
            as: "diag"
        }
    }
]);
