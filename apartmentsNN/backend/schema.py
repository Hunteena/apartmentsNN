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
  "dateFrom": '2023-05-01',
  "dateTo": '2023-05-02',
  "name": "John",
  "phone": "Doe",
  "email": "johndoe@example.com",
  "guests": 1,
  "apartment": 1
}
