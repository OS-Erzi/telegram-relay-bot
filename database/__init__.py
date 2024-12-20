from .database import Database

# Инициализация подключения к базе данных
db = Database()

# Экспорт основных функций или классов
__all__ = ['db']