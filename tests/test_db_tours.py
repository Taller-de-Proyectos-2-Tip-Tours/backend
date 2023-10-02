import os
import json

os.environ["TESTING"] = "True"

from db.tours_db import ToursCollection

#Get all tours devuelve los 2 tours presentes en la mockDB
def test_get_all_tours():
    collection = ToursCollection()
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 2

#Insert tour agrega 1 tour presentes a la mockDB
def test_insert_tour():
    collection = ToursCollection()
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 2
    collection.insert_tour({
        "name": "Cicloturismo en Buenos Aires",
        "duration": "02:00",
        "description": "Descubre los rincones ocultos de Buenos Aires en este paseo en bicicleta de 2 horas. Recorreremos parques, calles históricas y disfrutaremos de la brisa.",
        "minParticipants": 5,
        "maxParticipants": 15,
        "city": "Buenos Aires",
        "considerations": "Lleva tu bicicleta o alquila una en el lugar. Se proporcionarán cascos y chalecos de seguridad.",
        "language": "Español",
        "meetingPoint": "Parque de la Memoria",
        "dates": [
            {"date": "2023-10-09T16:00:00", "state": "abierto", "people": 0},
            {"date": "2023-10-11T18:00:00", "state": "abierto", "people": 0}
        ],
        "mainImage": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/...",
        "otherImages": [
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/...",
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."
        ],
        "lat": -34.540789,
        "lon": -58.464861,
        "guide": {
            "name": "Juan Pérez",
            "email": "juan.perez@example.com"
        }
    })
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 3
    collection.remove_tour("Cicloturismo en Buenos Aires")
