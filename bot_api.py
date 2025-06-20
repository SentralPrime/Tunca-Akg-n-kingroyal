import requests
import time
import random
from datetime import datetime
import json

class CasinoAPIBot:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.kingroyal.com"  # Casino sitesi URL'si
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'Origin': 'https://www.kingroyal.com',
            'Referer': 'https://www.kingroyal.com/casino'
        }
        self.session.headers.update(self.headers)
        self.bot_running = False
        self.round_count = 0
        
    def log_with_timestamp(self, message):
        """Zaman damgalı log mesajı"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def login(self, username, password):
        """Casino sitesine giriş yap"""
        login_url = f"{self.base_url}/api/auth/login"
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = self.session.post(login_url, json=login_data)
            if response.status_code == 200:
                self.log_with_timestamp("✅ Giriş başarılı!")
                return True
            else:
                self.log_with_timestamp(f"❌ Giriş başarısız: {response.status_code}")
                return False
        except Exception as e:
            self.log_with_timestamp(f"❌ Giriş hatası: {str(e)}")
            return False
            
    def get_game_session(self):
        """Oyun oturumu başlat"""
        game_url = f"{self.base_url}/api/casino/game/start"
        game_data = {
            "gameId": "spin2win",  # Oyun ID'si
            "currency": "TRY"
        }
        
        try:
            response = self.session.post(game_url, json=game_data)
            if response.status_code == 200:
                session_data = response.json()
                self.game_session_id = session_data.get('sessionId')
                self.log_with_timestamp("✅ Oyun oturumu başlatıldı!")
                return True
            else:
                self.log_with_timestamp(f"❌ Oyun oturumu başlatılamadı: {response.status_code}")
                return False
        except Exception as e:
            self.log_with_timestamp(f"❌ Oyun oturumu hatası: {str(e)}")
            return False
            
    def place_bet(self, bet_type, amount):
        """Bahis yap"""
        bet_url = f"{self.base_url}/api/casino/game/bet"
        bet_data = {
            "sessionId": self.game_session_id,
            "betType": bet_type,  # "TEK" veya "CIFT"
            "amount": amount
        }
        
        try:
            response = self.session.post(bet_url, json=bet_data)
            if response.status_code == 200:
                return True
            else:
                self.log_with_timestamp(f"❌ Bahis yapılamadı: {response.status_code}")
                return False
        except Exception as e:
            self.log_with_timestamp(f"❌ Bahis hatası: {str(e)}")
            return False
            
    def spin(self):
        """Çarkı çevir"""
        spin_url = f"{self.base_url}/api/casino/game/spin"
        spin_data = {
            "sessionId": self.game_session_id
        }
        
        try:
            response = self.session.post(spin_url, json=spin_data)
            if response.status_code == 200:
                result = response.json()
                self.log_with_timestamp(f"🎰 Sonuç: {result.get('result', 'Bilinmiyor')}")
                return result
            else:
                self.log_with_timestamp(f"❌ Çark çevrilemedi: {response.status_code}")
                return None
        except Exception as e:
            self.log_with_timestamp(f"❌ Çark hatası: {str(e)}")
            return None
            
    def play_round(self):
        """Bir round oyna"""
        self.round_count += 1
        self.log_with_timestamp(f"🎯 ROUND {self.round_count} başlıyor...")
        
        # TEK bahsi
        tek_amount = random.randint(1, 6)
        for i in range(tek_amount):
            if self.place_bet("TEK", 10):  # 10 TL bahis
                time.sleep(0.1)
        self.log_with_timestamp(f"✅ TEK butonuna ({tek_amount}) defa basıldı")
        
        time.sleep(1)
        
        # ÇİFT bahsi
        cift_amount = random.randint(1, 6)
        for i in range(cift_amount):
            if self.place_bet("CIFT", 10):  # 10 TL bahis
                time.sleep(0.1)
        self.log_with_timestamp(f"✅ ÇİFT butonuna ({cift_amount}) defa basıldı")
        
        time.sleep(1)
        
        # Çarkı çevir
        self.log_with_timestamp("✅ PLAY butonuna basıldı, işlemlerin bitmesi bekleniyor (27 saniye)...")
        result = self.spin()
        
        # 27 saniye bekle
        time.sleep(27)
        
        self.log_with_timestamp(f"🎉 ROUND {self.round_count} tamamlandı! Sonraki round hazırlanıyor...")
        time.sleep(3)
        
    def start_bot(self, username, password):
        """Bot'u başlat"""
        self.bot_running = True
        self.log_with_timestamp("🤖 Bot başlatılıyor...")
        
        # Giriş yap
        if not self.login(username, password):
            self.log_with_timestamp("❌ Giriş yapılamadı, bot durduruluyor!")
            self.bot_running = False
            return
            
        # Oyun oturumu başlat
        if not self.get_game_session():
            self.log_with_timestamp("❌ Oyun oturumu başlatılamadı, bot durduruluyor!")
            self.bot_running = False
            return
            
        # Ana döngü
        while self.bot_running:
            try:
                self.play_round()
            except Exception as e:
                self.log_with_timestamp(f"❌ Round hatası: {str(e)}")
                time.sleep(5)
                
    def stop_bot(self):
        """Bot'u durdur"""
        self.bot_running = False
        self.log_with_timestamp("🛑 Bot durduruluyor...")

# Test için
if __name__ == "__main__":
    bot = CasinoAPIBot()
    # NOT: Gerçek kullanıcı adı ve şifre ile değiştirin
    bot.start_bot("kullanici_adi", "sifre") 