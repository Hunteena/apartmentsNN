APARTMENT_SCHEMA_EXAMPLE = {
    "id": 0,
    "images": [
        [
            {
                "photo": "string",
                "name": "string",
                "altName": "string",
                "group": 0
            }
        ]
    ],
    "comfort": [
        {
            "type": "string",
            "description": "string"
        }
    ],
    "location": {
        "url": "string",
        "desc": [
            "string"
        ]
    },
    "name": "string",
    "title": "string",
    "address": "string",
    "description": "string",
    "shortDescription": [
        "string"
    ],
    "price": 2147483647,
    "capacity": 32767,
    "owner": 0,
    "detailedCharacteristic": [
        {
            "name": "string",
            "data": "string"
        }
    ]
}

BOOKING_SCHEMA_EXAMPLE = {
  "dateFrom": 1688191200000,
  "dateTo": 1688277600000,
  "name": "string",
  "phone": "string",
  "email": "user@example.com",
  "guests": 32767,
  "apartment": 0
}
