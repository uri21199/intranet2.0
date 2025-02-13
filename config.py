from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# Configuración de la base de datos
DATABASE_CONFIG = {
    'user': 'postgres',  # Reemplaza con tu usuario de PostgreSQL
    'password': '348287',  # Reemplaza con tu contraseña de PostgreSQL
    'host': 'localhost',  # Cambia esto si no estás trabajando en localhost
    'port': 5432,  # Puerto estándar de PostgreSQL
    'database': 'wmms'  # Nombre de tu base de datos
}

# Crear la URL de conexión
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
               f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?client_encoding=utf8"


# Configuración del motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Definir `Base` para que los modelos hereden de esta clase
Base = declarative_base()

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Verificar conexión a la base de datos
try:
    with engine.connect() as connection:
        print("✅ Conexión a la base de datos exitosa.")
except OperationalError as e:
    print("❌ Error al conectar con la base de datos:", e)
