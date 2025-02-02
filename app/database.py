from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URL

# Создаем асинхронный движок для подключения к БД
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем фабрику сессий
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency для получения сессии в эндпоинтах
async def get_db():
    async with async_session() as session:
        yield session
