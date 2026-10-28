import sys
from pathlib import Path

# Resolve project root and backend paths
API_DIR = Path(__file__).resolve().parent
ROOT_DIR = API_DIR.parent
BACKEND_DIR = ROOT_DIR / "backend"

# Ensure backend modules ('app.main', etc.) can be imported
for p in [str(BACKEND_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app

# Expose ASGI application for Vercel Python runtime
__all__ = ["app"]
