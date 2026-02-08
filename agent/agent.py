# agent/agent.py
import time
import configparser
import requests
import platform
import psutil
from screenshot import capture_screenshot


class MonitoringAgent:
    """
    Monitoring Agent - Windows / Mac / Linux
    """

    def __init__(self, config_path='config.ini'):
        print("🚀 Monitoring Agent boshlanyapti...")

        # Config yuklash
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Ma'lumotlar
        self.kassa_id = self.config['KASSA']['ID']
        self.viloyat = self.config['KASSA']['VILOYAT']
        self.pc_name = self.config['KASSA']['PC_NAME']
        self.secret_key = self.config['KASSA']['SECRET_KEY']

        # Server
        self.server_url = self.config['SERVER']['URL']

        # Screenshot sozlamalari
        self.screenshot_enabled = self.config['SCREENSHOT'].getboolean('ENABLED')
        self.screenshot_interval = self.config['SCREENSHOT'].getint('INTERVAL')
        self.screenshot_quality = self.config['SCREENSHOT'].getint('QUALITY')

        print(f"✅ Kassa: {self.kassa_id}")
        print(f"✅ PC: {self.pc_name}")
        print(f"✅ Server: {self.server_url}")
        print(f"✅ Screenshot interval: {self.screenshot_interval}s")

    def get_system_info(self):
        """Tizim ma'lumotlari"""
        try:
            disk = '/'
            if platform.system() == 'Windows':
                disk = 'C:'

            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage(disk).percent,
                'uptime': time.time() - psutil.boot_time()
            }
        except Exception as e:
            print(f"System info error: {e}")
            return {}

    def send_heartbeat(self):
        """Server ga heartbeat yuborish"""
        try:
            url = f"{self.server_url}/api/heartbeat"
            payload = {
                'kassa_id': self.kassa_id,
                'viloyat': self.viloyat,
                'pc_name': self.pc_name,
                'timestamp': time.time(),
                'system_info': self.get_system_info()
            }

            response = requests.post(url, json=payload, timeout=5)

            if response.status_code == 200:
                print("💓 Heartbeat yuborildi")
                return True
            else:
                print(f"⚠️ Heartbeat xato: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Heartbeat xato: {e}")
            return False

    def upload_screenshot(self, screenshot_data):
        """Screenshot yuklash"""
        try:
            url = f"{self.server_url}/api/upload/screenshot"

            files = {
                'screenshot': ('screenshot.jpg', screenshot_data, 'image/jpeg')
            }

            data = {
                'kassa_id': self.kassa_id,
                'viloyat': self.viloyat,
                'timestamp': time.time()
            }

            response = requests.post(url, files=files, data=data, timeout=30)

            if response.status_code == 200:
                print("📤 Screenshot yuklandi")
                return True
            else:
                print(f"⚠️ Upload xato: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Upload xato: {e}")
            return False

    def run(self):
        """Asosiy loop"""
        print("\n▶️ Agent ishga tushdi!")
        print("Ctrl+C - to'xtatish\n")

        try:
            while True:
                # Screenshot
                if self.screenshot_enabled:
                    screenshot_data = capture_screenshot(self.screenshot_quality)
                    if screenshot_data:
                        # Serverga yuborish
                        self.upload_screenshot(screenshot_data)

                        # Localga saqlash (debug uchun)
                        timestamp = int(time.time())
                        filename = f"data/screenshot_{timestamp}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(screenshot_data)
                        print(f"💾 Saqlandi: {filename}")

                # Heartbeat
                self.send_heartbeat()

                print(f"⏳ {self.screenshot_interval} sekund kutish...\n")
                time.sleep(self.screenshot_interval)

        except KeyboardInterrupt:
            print("\n⏹️ Agent to'xtatildi")


if __name__ == '__main__':
    agent = MonitoringAgent()
    agent.run()
