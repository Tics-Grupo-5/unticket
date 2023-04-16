FILTERS = {
    'solicitudes': {
        'id': {
            'column': 0,
            'unique': True,
        },
        'estado': {
            'column': 1,
            'unique': False,
        },
        'nombre_solicitante': {
            'column': 2,
            'unique': False,
        },
        'certificado': {
            'column': 3,
            'unique': False,
        },
        'encargado': {
            'column': 4,
            'unique': False,
        },
    },
    'mis_solicitudes': {
        'id': {
            'column': 0,
            'unique': True,
        },
        'estado': {
            'column': 1,
            'unique': False,
        },
        'certificado': {
            'column': 2,
            'unique': False,
        },
        'número_pago': {
            'column': 3,
            'unique': False,
        },
        'observaciones': {
            'column': 4,
            'unique': False,
        },
    },
    'certificados': {
        'nombre': {
            'column': 0,
            'unique': True,
        },
        'grupo': {
            'column': 1,
            'unique': False,
        },
    },
    'usuarios': {
        'username': {
            'column': 0,
            'unique': True,
        }
    },
}
