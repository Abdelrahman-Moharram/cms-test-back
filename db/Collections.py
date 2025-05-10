page = {
    "bsonType": "object",
    "required": ["title"],
    "properties": {
        "title": {
            "bsonType": "string",
            "description": "must be a string and is required",
            "minimum": 2,
        }
    }
}


section = {
    "bsonType": "object",
    "required": ["order"],
    "properties": {
        "title": {
            "bsonType": "string",
            "description": "must be a string and is required",
            "minimum": 2,
        },
        'order':{
            'bsonType': 'number'
        },
        "width":{
            "bsonType": "string",
            "description": "must be a string and is required",
            "minimum": 2,
        }

    }
}
