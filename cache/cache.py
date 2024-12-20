import asyncio
from core import settings
from typing import Dict, Set

# Создаем множество для хранения белого списка пользователей
whitelist_users: Set[int] = set()
# Словарь для кэширования результатов проверки блокировки
block_cache: Dict[int, bool] = {}

async def clear_cache_periodically():
    while True:
        await asyncio.sleep(settings.CACHE_LIFETIME)
        block_cache.clear()