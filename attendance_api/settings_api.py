from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi import Request
import os
import json
from pydantic import BaseModel

router = APIRouter()

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

class SettingsModel(BaseModel):
    app: dict
    device: dict

@router.get("/api/settings.json")
def get_settings_json():
    if not os.path.exists(SETTINGS_PATH):
        raise HTTPException(status_code=404, detail="settings.json not found")
    return FileResponse(SETTINGS_PATH, media_type="application/json")

@router.post("/api/settings.json")
def save_settings_json(settings: SettingsModel):
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings.dict(), f, indent=2)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
