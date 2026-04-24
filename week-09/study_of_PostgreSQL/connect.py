import psycopg2 # или просто psycopg
from config_for_study import load_config

def connect(config):
    """ Подключение к серверу PostgreSQL """
    try:
        # **config разворачивает словарь в аргументы: host=..., database=...
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    config = load_config()
    connect(config)