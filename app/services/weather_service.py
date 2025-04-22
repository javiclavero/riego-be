import requests
from app.config import OPENWEATHERMAP_API_KEY
from datetime import datetime, timedelta

def fetch_weather_data(latitude: float, longitude: float, location_id: int, location_name: str):
    base_url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
    now = datetime.now()
    start_time = int((now - timedelta(days=30)).timestamp())
    end_time = int(now.timestamp())
    historical_data = []

    for day_offset in range(30):
        past_date = now - timedelta(days=day_offset)
        timestamp = int(past_date.timestamp())
        params = {
            "lat": latitude,
            "lon": longitude,
            "dt": timestamp,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if "hourly" in data:
                midday_hour = 12
                closest_record = min(data["hourly"], key=lambda x: abs(datetime.fromtimestamp(x["dt"]).hour - midday_hour))
                historical_data.append({
                    "PrecLocId": location_id,
                    "LocName": location_name,
                    "Precipitation": closest_record.get("rain", {}).get("1h", 0) if "rain" in closest_record else 0,
                    "TempMax": closest_record["temp"],
                    "TempMin": closest_record["temp"],
                    "Date": datetime.fromtimestamp(closest_record["dt"]).strftime('%Y-%m-%d')
                })
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos para ({latitude}, {longitude}) en {past_date}: {e}")
            continue
        except KeyError as e:
            print(f"Error al procesar datos para ({latitude}, {longitude}) en {past_date}: Falta clave {e}")
            continue
        # import time
        # time.sleep(1)
    return historical_data

def save_weather_data(weather_data_list):
    db_conn = get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            sql = "INSERT INTO tblWeatherData (WeaLocId, WeaRain, WeaTempMax, WeaTempMin, WeaDate) VALUES (%s, %s, %s, %s, %s)"
            values = [(data["PrecLocId"], data["Precipitation"], data["TempMax"], data["TempMin"], data["Date"]) for data in weather_data_list]
            cursor.executemany(sql, values)
            db_conn.commit()
            print(f"{cursor.rowcount} registros insertados en tblWeatherData.")
        except mysql.connector.Error as err:
            print(f"Error al insertar en la base de datos: {err}")
            db_conn.rollback()
        finally:
            cursor.close()
            db_conn.close()