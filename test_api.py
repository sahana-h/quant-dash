import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 