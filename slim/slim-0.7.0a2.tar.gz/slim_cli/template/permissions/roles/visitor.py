from slim.ext.permission import Ability, A

visitor = Ability({
    'example': {
        'id': {A.READ, A.QUERY},
        'state': {A.READ},
    },
    'user': {
        'id': {A.QUERY, A.READ},
        'nickname': {A.READ},
        'state': {A.READ},
        'time': {A.READ},
    }
})
