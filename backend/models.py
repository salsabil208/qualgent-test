# backend/models.py
from pydantic import BaseModel

class Job(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 0
    target: str   # "emulator", "device", "browserstack"
