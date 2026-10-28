import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Determine environment
IS_VERCEL = bool(os.getenv("VERCEL"))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if IS_VERCEL:
        # On Vercel Serverless, only /tmp is writable
        tmp_db = Path("/tmp/expense_optimizer.db")
        if not tmp_db.exists():
            # Attempt to copy seed database from repository if available
            base_candidates = [
                Path(__file__).resolve().parent.parent / "expense_optimizer.db",
                Path(__file__).resolve().parent.parent.parent / "backend" / "expense_optimizer.db",
                Path("/var/task/backend/expense_optimizer.db"),
                Path("/var/task/expense_optimizer.db"),
            ]
            for candidate in base_candidates:
                if candidate.exists() and candidate.is_file():
                    try:
                        shutil.copyfile(str(candidate), str(tmp_db))
                        break
                    except Exception:
                        pass
        DATABASE_URL = f"sqlite:///{tmp_db}"
    else:
        DATABASE_URL = "sqlite:///./expense_optimizer.db"
elif DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy 2.0 requires postgresql:// instead of postgres://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

