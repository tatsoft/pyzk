from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Request
import os
import json
from pydantic import BaseModel

router = APIRouter()

# Get the absolute path to settings.json in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')

class SettingsModel(BaseModel):
    app: dict
    device: dict

@router.get("/api/settings.json")
def get_settings_json():
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"Settings file not found at: {SETTINGS_PATH}")
            raise HTTPException(status_code=404, detail=f"settings.json not found at {SETTINGS_PATH}")
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(data)
    except Exception as e:
        print(f"Error loading settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/settings.json")
def save_settings_json(settings: SettingsModel):
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings.dict(), f, indent=2)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
