# server/main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
from datetime import datetime
import json

app = FastAPI(title="Gaz Monitoring API")

# CORS (Frontend uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folders
os.makedirs("uploads/screenshots", exist_ok=True)
os.makedirs("data", exist_ok=True)

# In-memory database (SODDA!)
kassas_db = {}

# Static files (screenshots)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Gaz Monitoring API", "version": "1.0"}


@app.post("/api/heartbeat")
async def heartbeat(data: dict):
    """Agent heartbeat"""
    kassa_id = data.get('kassa_id')
    
    if kassa_id not in kassas_db:
        kassas_db[kassa_id] = {}
    
    kassas_db[kassa_id].update({
        'kassa_id': kassa_id,
        'viloyat': data.get('viloyat', 'Unknown'),
        'pc_name': data.get('pc_name', 'Unknown'),
        'status': 'online',
        'last_seen': datetime.now().isoformat(),
        'system_info': data.get('system_info', {}),
        'ip_address': '192.168.1.45'  # TODO: real IP
    })
    
    print(f"💓 Heartbeat: {kassa_id}")
    return {"status": "ok"}


@app.post("/api/upload/screenshot")
async def upload_screenshot(
    screenshot: UploadFile = File(...),
    kassa_id: str = Form(...),
    viloyat: str = Form(...),
    timestamp: str = Form(...)
):
    """Screenshot yuklash"""
    
    # Save screenshot
    filename = f"{kassa_id}_{int(float(timestamp))}.jpg"
    filepath = f"uploads/screenshots/{filename}"
    
    with open(filepath, "wb") as f:
        content = await screenshot.read()
        f.write(content)
    
    # Update kassa
    if kassa_id not in kassas_db:
        kassas_db[kassa_id] = {}
    
    if 'screenshots' not in kassas_db[kassa_id]:
        kassas_db[kassa_id]['screenshots'] = []
    
    kassas_db[kassa_id]['screenshots'].append({
        'filename': filename,
        'filepath': filepath,
        'url': f"/uploads/screenshots/{filename}",
        'timestamp': timestamp,
        'size': len(content)
    })
    
    # Keep only last 50
    kassas_db[kassa_id]['screenshots'] = kassas_db[kassa_id]['screenshots'][-50:]
    
    print(f"📸 Screenshot yuklandi: {kassa_id} - {filename}")
    return {"status": "ok", "filename": filename}


@app.get("/api/kassas")
async def get_kassas():
    """Barcha kassalar"""
    kassas = []
    
    for kassa_id, data in kassas_db.items():
        # Check if online (last 60 seconds)
        last_seen = datetime.fromisoformat(data.get('last_seen', datetime.now().isoformat()))
        is_online = (datetime.now() - last_seen).seconds < 60
        
        kassas.append({
            'id': kassa_id,
            'kassa_id': kassa_id,
            'pc_name': data.get('pc_name', f'KASSA_{kassa_id}_PC'),
            'ip_address': data.get('ip_address', '192.168.1.x'),
            'viloyat': data.get('viloyat', 'Unknown'),
            'status': 'online' if is_online else 'offline',
            'last_seen': data.get('last_seen'),
            'system_info': data.get('system_info', {}),
            'screenshot_count': len(data.get('screenshots', []))
        })
    
    return {'kassas': kassas, 'total': len(kassas)}


@app.get("/api/kassa/{kassa_id}")
async def get_kassa(kassa_id: str):
    """Bitta kassa"""
    if kassa_id not in kassas_db:
        return JSONResponse(
            status_code=404,
            content={"error": "Kassa topilmadi"}
        )
    
    data = kassas_db[kassa_id]
    
    # Check if online
    last_seen = datetime.fromisoformat(data.get('last_seen', datetime.now().isoformat()))
    is_online = (datetime.now() - last_seen).seconds < 60
    
    return {
        'kassa_id': kassa_id,
        'pc_name': data.get('pc_name'),
        'ip_address': data.get('ip_address'),
        'viloyat': data.get('viloyat'),
        'status': 'online' if is_online else 'offline',
        'last_seen': data.get('last_seen'),
        'system_info': data.get('system_info', {}),
        'screenshots': data.get('screenshots', [])[-10:]  # Last 10
    }


@app.get("/api/kassa/{kassa_id}/screenshots")
async def get_kassa_screenshots(kassa_id: str):
    """Kassa screenshotlari"""
    if kassa_id not in kassas_db:
        return JSONResponse(
            status_code=404,
            content={"error": "Kassa topilmadi"}
        )
    
    screenshots = kassas_db[kassa_id].get('screenshots', [])
    return {'screenshots': screenshots, 'total': len(screenshots)}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Server ishga tushmoqda...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📖 Docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)