import psycopg2
from config import params

def conn():
    try:
        return psycopg2.connect(**params)
    except Exception as error:
        print(f"Ошибка при подключении к базе: {error}")
        return None