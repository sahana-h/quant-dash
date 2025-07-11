import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.models.base import engine
from backend.models import models


def init_database():
    """Create all database tables"""
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_database()
    print("Database tables created successfully!")