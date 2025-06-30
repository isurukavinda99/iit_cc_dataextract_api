import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
SessionLocal = None
logger = logging.getLogger(__name__)


def init_db():
    global SessionLocal

    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ.get("DB_PORT", "8123")
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ.get("DB_USER", "default")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

    # Use native protocol if port is 9000, otherwise HTTP
    protocol = "native" if DB_PORT == "9000" else "http"

    DATABASE_URL = f"clickhouse+{protocol}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))

        SessionLocal = sessionmaker(bind=engine, autoflush=False)
        logger.info(f"Successfully connected to ClickHouse at {DB_HOST}:{DB_PORT}")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to ClickHouse: {str(e)}")
        raise


def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()