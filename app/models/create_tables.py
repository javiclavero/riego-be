from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database as create_db_utils
from app.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
from app.models.database import Base, DATABASE_URL  # Importa la URL sin la base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    if not database_exists(engine.url):
        create_db_utils(engine.url)
        print(f"Base de datos '{DATABASE_NAME}' creada.")
    else:
        print(f"La base de datos '{DATABASE_NAME}' ya existe.")
    Base.metadata.create_all(bind=engine)
    print("Tablas de la base de datos creadas.")

if __name__ == "__main__":
    create_database()