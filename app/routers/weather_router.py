from fastapi import APIRouter, Depends
from app.services import weather_service, location_service  # Importa location_service

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/process")
async def process_weather():
    locations = location_service.get_locations_from_db()  # Usa la función del servicio
    if locations:
        all_weather_data = []
        for location in locations:
            loc_id = location.get("LocId")
            loc_name = location.get("LocName")
            latitude = location.get("LocLatitude")
            longitude = location.get("LocLongitude")
            if all(v is not None for v in [latitude, longitude, loc_id, loc_name]):
                weather_data = weather_service.fetch_weather_data(latitude, longitude, loc_id, loc_name)
                all_weather_data.extend(weather_data)
            else:
                print(f"Advertencia: Datos de localización incompletos para {location}")
        if all_weather_data:
            weather_service.save_weather_data(all_weather_data)
            return {"message": f"Proceso completado. Se intentaron insertar datos para {len(locations)} localizaciones."}
        else:
            return {"message": "No se obtuvieron datos meteorológicos para insertar."}
    else:
        return {"message": "No se pudieron obtener las localizaciones."}