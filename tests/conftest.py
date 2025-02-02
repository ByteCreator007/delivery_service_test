import asyncio
import pytest
from app.database import engine  # импорт вашего async engine

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    # Завершаем асинхронные генераторы
    loop.run_until_complete(loop.shutdown_asyncgens())
    # Отменяем все оставшиеся задачи в loop, чтобы они не пытались выполниться после закрытия
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    # Явно закрываем engine, чтобы все соединения вернулись в пул и корректно завершились
    loop.run_until_complete(engine.dispose())
    loop.close()
