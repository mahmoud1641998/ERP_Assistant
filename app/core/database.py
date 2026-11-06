
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# AI Assistant Database URL
ai_database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.AI_DB_USER,
    password=settings.AI_DB_PASSWORD,
    host=settings.AI_DB_HOST,
    port=settings.AI_DB_PORT,
    database=settings.AI_DB_NAME,
    query={"charset": "utf8mb4"}
)


# ERP Database URL
erp_database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.ERP_DB_USER,
    password=settings.ERP_DB_PASSWORD,
    host=settings.ERP_DB_HOST,
    port=settings.ERP_DB_PORT,
    database=settings.ERP_DB_NAME,
    query={"charset": "utf8mb4"}
)


# AI Assistant Database Engine
ai_engine = create_engine(
    ai_database_url,
    pool_pre_ping=True,
    echo=False
)


# ERP Database Engine
erp_engine = create_engine(
    erp_database_url,
    pool_pre_ping=True,
    echo=False
)


# AI Assistant Database Session
AISessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ai_engine
)


# ERP Database Session
ERPSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=erp_engine
)





def get_db() -> Generator[Session, None, None]:
    db = AISessionLocal()

    try:
        yield db
    finally:
        db.close()
