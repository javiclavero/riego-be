from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Location(Base):
    __tablename__ = "tblLocations"

    LocId = Column(Integer, primary_key=True, index=True)
    LocName = Column(String(255))
    LocLatitude = Column(Float)
    LocLongitude = Column(Float)

class WeatherData(Base):
    __tablename__ = "tblWeatherData"

    WeaId = Column(Integer, primary_key=True, index=True)
    WeaLocId = Column(Integer)  # Clave foránea (la definiremos explícitamente luego)
    WeaRain = Column(Float)
    WeaTempMax = Column(Float)
    WeaTempMin = Column(Float)
    WeaDate = Column(Date)