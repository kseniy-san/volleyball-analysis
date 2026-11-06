from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Указываем путь к файлу базы данных SQLite (он создастся в корне проекта)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Создаем движок (engine) для подключения к БД
# check_same_thread=False нужен специально для SQLite, чтобы с ней мог работать FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем фабрику сессий (через нее мы будем делать запросы к БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс, от которого будут наследоваться все наши модели
Base = declarative_base()