import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .models import Base

logging.basicConfig(level=logging.INFO)

def get_database_url():
    url = os.getenv('DATABASE_URL')
    if not url:
        logging.error("DATABASE_URL is not set")
        raise ValueError("DATABASE_URL is not set")
    return url

def create_engine_instance():
    return create_engine(get_database_url())

def create_tables(engine):
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully.")
    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    engine = create_engine_instance()
    create_tables(engine)