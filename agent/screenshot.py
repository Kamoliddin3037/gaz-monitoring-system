# agent/screenshot.py
import io
import time
from PIL import ImageGrab

def capture_screenshot(quality=75):
    """
    Screenshot olish
    Returns: bytes (JPEG format)
    """
    try:
        # Screenshot
        screenshot = ImageGrab.grab()
        
        # RGBA → RGB convert (MUHIM!)
        if screenshot.mode == 'RGBA':
            screenshot = screenshot.convert('RGB')
        
        # Resize (katta bo'lsa)
        max_size = (1920, 1080)
        screenshot.thumbnail(max_size)
        
        # JPEG ga convert
        buffer = io.BytesIO()
        screenshot.save(buffer, format='JPEG', quality=quality, optimize=True)
        screenshot_bytes = buffer.getvalue()
        
        print(f"✅ Screenshot: {len(screenshot_bytes)} bytes")
        return screenshot_bytes
        
    except Exception as e:
        print(f"❌ Screenshot xato: {e}")
        return None


if __name__ == '__main__':
    # Test
    print("📸 Screenshot test...")
    data = capture_screenshot()
    if data:
        # Faylga saqlash
        with open('test_screenshot.jpg', 'wb') as f:
            f.write(data)
        print("✅ test_screenshot.jpg saqlandi")