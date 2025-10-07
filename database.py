from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker
DB = "sqlite:///./test.db"

engine = create_engine(DB)

engine = create_engine(DB, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


mapper_registry = registry()
Base = mapper_registry.generate_base()

