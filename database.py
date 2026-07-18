import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

async def create_db_connection()-> asyncpg.Connection:
    try:
        return await asyncpg.connect(
            host=db_host,
            database=db_name,
            user=db_username,
            password=db_password,
            port=int(db_port)
        )

    except Exception as e:
        print(f"Database connection occurred : - {str(e)}")