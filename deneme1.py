from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
import os
import sys
import tempfile
import uuid
from datetime import datetime

# Railway ortamı için logging
def log_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    sys.stdout.flush()  # Railway için immediate output

random_max = 6
random_min = 1
class BahisButtonClicker:
    def __init__(self):
        self.driver = None
        self.url = "https://mighty.hub.xpressgaming.net/Launcher?token=kerFejSb71pofJRcMwNnz0OSpu4mlEGU&game=10159&backurl=https%3A%2F%2Fkingroyal619.com&mode=1&language=tr&group=master&clientPlatform=desktop&cashierurl=https%3A%2F%2Fkingroyal619.com&h=e9abbf9a87f6d06462f80ce10af52b7c"
        self.session_active = False
        
        # 503 numaralı buton bilgileri (TEK butonu)
        self.tek_button = {
            'numara': 503,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'TEK',
            'class': 'spin2win-box__market-display grid grid-middle grid-center',
            'konum_x': 805,
            'konum_y': 424,
            'tur': 'Bahis Seçeneği'
        }
        
        # 500 numaralı buton bilgileri (ÇİFT butonu)
        self.cift_button = {
            'numara': 500,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'ÇİFT',
            'class': 'spin2win-box__market-display grid grid-middle grid-center',
            'konum_x': 604,
            'konum_y': 424,
            'tur': 'Bahis Seçeneği'
        }
        
        # 504 numaralı buton bilgileri (OYNA butonu)
        self.play_button = {
            'numara': 504,
            'context': 'Frame 1',
            'tag': 'DIV',
            'text': 'Boş',
            'class': 'grid grid-middle grid-center casino-game-play-button icon-play-minimal',
            'id': 'game-play-button',
            'konum_x': 1130,
            'konum_y': 556,
            'tur': 'Oyun Butonu'
        }
        
    def setup_driver(self):
        """Chrome WebDriver'ı kurulum - Railway memory optimized"""
        chrome_options = Options()
        
        # Railway için agresif memory ayarları
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        
        # User data directory conflict'ini çöz - unique directory
        import tempfile
        import uuid
        temp_dir = tempfile.mkdtemp()
        unique_user_data = os.path.join(temp_dir, f"chrome_user_data_{uuid.uuid4().hex[:8]}")
        chrome_options.add_argument(f"--user-data-dir={unique_user_data}")
        
        # Chrome stability için kritik ayarlar
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
        
        # Chrome session stability için
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--force-fieldtrials=*BackgroundTracing/default/")
        
        # DevTools connection stability
        chrome_options.add_argument("--remote-debugging-port=0")  # Random port
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Process ayarları - tek process yerine daha stable
        chrome_options.add_argument("--renderer-process-limit=1")
        chrome_options.add_argument("--max-active-webgl-contexts=1")
        
        # Memory optimization - Railway için kritik
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu-logging")
        chrome_options.add_argument("--silent")
        
        # Shared memory ayarları
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        
        # Process ayarları
        chrome_options.add_argument("--max_old_space_size=2048")
        chrome_options.add_argument("--renderer-process-limit=1")
        chrome_options.add_argument("--max-active-webgl-contexts=1")
        
        # Chrome binary path'i belirt
        chrome_binary_locations = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable", 
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium"
        ]
        
        for binary_path in chrome_binary_locations:
            if os.path.exists(binary_path):
                chrome_options.binary_location = binary_path
                log_with_timestamp(f"🔧 Chrome binary bulundu: {binary_path}")
                break
        
        # Render ortamı tespiti
        if os.environ.get('RENDER_ENVIRONMENT') or os.environ.get('PORT'):
            log_with_timestamp("🎨 Render ortamı tespit edildi - Memory optimized ayarlar")
            # Daha aggressive memory limits
            chrome_options.add_argument("--memory-pressure-off")
            chrome_options.add_argument("--max_old_space_size=1024")
            chrome_options.add_argument("--optimize-for-size")
        
        log_with_timestamp("🔧 Chrome Memory Optimized mode aktif")
        
        try:
            # ChromeDriver service ayarları
            chromedriver_paths = [
                "/usr/local/bin/chromedriver",
                "/usr/bin/chromedriver",
                os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
            ]
            
            chromedriver_path = None
            for path in chromedriver_paths:
                if os.path.exists(path):
                    chromedriver_path = path
                    log_with_timestamp(f"🔧 ChromeDriver bulundu: {path}")
                    break
            
            if chromedriver_path:
                # Service ayarları - timeout artırıldı
                service = Service(
                    chromedriver_path,
                    service_args=['--verbose', '--whitelisted-ips=']
                )
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                log_with_timestamp("🚀 Sistem ChromeDriver kullanılıyor...")
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Daha küçük pencere boyutu
            self.driver.set_window_size(1280, 720)
            
            # Connection timeout ayarları
            self.driver.implicitly_wait(30)
            self.driver.set_page_load_timeout(60)
            
            log_with_timestamp("✅ Chrome WebDriver başlatıldı (Stability Optimized)")
            
            # Test connection with retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    log_with_timestamp(f"🔍 Chrome connection test (deneme {attempt + 1}/{max_retries})...")
                    user_agent = self.driver.execute_script("return navigator.userAgent")
                    log_with_timestamp(f"✅ Chrome connection OK! User Agent: {user_agent[:50]}...")
                    break
                except Exception as e:
                    log_with_timestamp(f"⚠️ Connection test {attempt + 1} başarısız: {str(e)}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2)
            
        except Exception as e:
            log_with_timestamp(f"❌ Chrome WebDriver başlatılırken hata: {str(e)}")
            # Hata durumunda debug bilgileri
            log_with_timestamp("🔍 Debug bilgileri:")
            log_with_timestamp(f"   - CHROME_BIN: {os.environ.get('CHROME_BIN', 'Tanımlı değil')}")
            log_with_timestamp(f"   - CHROMEDRIVER_PATH: {os.environ.get('CHROMEDRIVER_PATH', 'Tanımlı değil')}")
            log_with_timestamp(f"   - RENDER_ENVIRONMENT: {os.environ.get('RENDER_ENVIRONMENT', 'Tanımlı değil')}")
            
            # Retry mechanism - bir kez daha dene
            log_with_timestamp("🔄 Tekrar deneniyor...")
            try:
                # Daha minimal ayarlarla dene
                minimal_options = Options()
                minimal_options.add_argument("--headless=new")
                minimal_options.add_argument("--no-sandbox")
                minimal_options.add_argument("--disable-dev-shm-usage")
                minimal_options.add_argument("--single-process")
                minimal_options.add_argument("--window-size=800,600")
                
                if chromedriver_path:
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=minimal_options)
                else:
                    self.driver = webdriver.Chrome(options=minimal_options)
                
                self.driver.set_window_size(800, 600)
                log_with_timestamp("✅ Chrome WebDriver başlatıldı (Minimal Mode)")
                
            except Exception as retry_error:
                log_with_timestamp(f"❌ Retry de başarısız: {str(retry_error)}")
                raise
    
    def is_session_active(self):
        """Chrome session'ının aktif olup olmadığını kontrol et"""
        try:
            if not self.driver:
                return False
            # Basit bir JavaScript komutu çalıştırarak session'ı test et
            self.driver.execute_script("return document.readyState")
            self.session_active = True
            return True
        except Exception as e:
            log_with_timestamp(f"⚠️ Session kontrolü başarısız: {str(e)}")
            self.session_active = False
            return False
    
    def restart_session_if_needed(self):
        """Gerekirse session'ı yeniden başlat"""
        if not self.is_session_active():
            log_with_timestamp("🔄 Session aktif değil, yeniden başlatılıyor...")
            try:
                if self.driver:
                    self.driver.quit()
            except:
                pass
            self.setup_driver()
            self.load_page()
            log_with_timestamp("✅ Session yeniden başlatıldı!")
        
    def load_page(self):
        """Sayfayı yükle"""
        log_with_timestamp("🌐 Casino sitesine gidiliyor...")
        try:
            self.driver.get(self.url)
            
            log_with_timestamp("⏳ Sayfa yükleniyor (15 saniye bekleniyor)...")
            time.sleep(15)
            
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            log_with_timestamp("✅ Sayfa tamamen yüklendi")
        except Exception as e:
            log_with_timestamp(f"❌ Sayfa yüklenirken hata: {str(e)}")
            raise
        
    def switch_to_game_frame(self):
        """Oyun frame'ine geç"""
        log_with_timestamp("🖼️ Oyun frame'ine geçiliyor...")
        
        try:
            # Ana sayfaya dön
            self.driver.switch_to.default_content()
            
            # İlk iframe'i bul ve geç
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            if len(frames) > 0:
                self.driver.switch_to.frame(frames[0])
                log_with_timestamp("✅ Frame 1'e geçildi")
                time.sleep(3)
            else:
                log_with_timestamp("❌ Frame bulunamadı!")
        except Exception as e:
            log_with_timestamp(f"❌ Frame geçişinde hata: {str(e)}")
            
    def find_and_click_tek_button(self):
        """TEK butonunu bul ve rastgele sayıda tıkla"""
        click_count = random.randint(1, random_max)
        log_with_timestamp(f"🎯 {self.tek_button['numara']} numaralı '{self.tek_button['text']}' butonu aranıyor...")
        log_with_timestamp(f"🎲 Rastgele tıklama sayısı: {click_count}")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"div.spin2win-box__market-display:contains('{self.tek_button['text']}')",
            f"div[class*='spin2win-box__market-display']",
            f"*:contains('{self.tek_button['text']}')",
            "div.spin2win-box__market-display"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                if ":contains" in selector:
                    # JavaScript ile contains kullan
                    elements = self.driver.execute_script(f"""
                        return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                            el => el.textContent.trim() === '{self.tek_button['text']}'
                        );
                    """)
                    
                    if elements and len(elements) > 0:
                        element = elements[0]
                        log_with_timestamp(f"   ✅ JavaScript ile '{self.tek_button['text']}' butonu bulundu!")
                        
                        # Element bilgilerini göster
                        text = self.driver.execute_script("return arguments[0].textContent.trim();", element)
                        class_name = self.driver.execute_script("return arguments[0].className;", element)
                        location = self.driver.execute_script("return {x: arguments[0].getBoundingClientRect().left, y: arguments[0].getBoundingClientRect().top};", element)
                        
                        log_with_timestamp(f"   📊 Buton Bilgileri:")
                        log_with_timestamp(f"      Text: {text}")
                        log_with_timestamp(f"      Class: {class_name}")
                        log_with_timestamp(f"      Konum: x={int(location['x'])}, y={int(location['y'])}")
                        
                        # Çoklu tıklama işlemi
                        log_with_timestamp(f"   🖱️ '{self.tek_button['text']}' butonuna {click_count} kez tıklanıyor...")
                        
                        try:
                            # JavaScript ile çoklu tıkla
                            for i in range(click_count):
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                            log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                            button_found = True
                            break
                            
                        except Exception as click_error:
                            log_with_timestamp(f"   ❌ Tıklama hatası: {str(click_error)}")
                            
                else:
                    # Normal CSS selector
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text == self.tek_button['text']:
                                    log_with_timestamp(f"   ✅ '{self.tek_button['text']}' butonu bulundu!")
                                    
                                    # Element bilgilerini göster
                                    class_name = element.get_attribute('class')
                                    location = element.location
                                    
                                    log_with_timestamp(f"   📊 Buton Bilgileri:")
                                    log_with_timestamp(f"      Text: {text}")
                                    log_with_timestamp(f"      Class: {class_name}")
                                    log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                                    
                                    # Çoklu tıklama işlemi
                                    log_with_timestamp(f"   🖱️ '{self.tek_button['text']}' butonuna {click_count} kez tıklanıyor...")
                                    
                                    try:
                                        for i in range(click_count):
                                            element.click()
                                            log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} normal tıklama başarılı!")
                                        button_found = True
                                        break
                                        
                                    except:
                                        # JavaScript ile çoklu tıkla
                                        for i in range(click_count):
                                            self.driver.execute_script("arguments[0].click();", element)
                                            log_with_timestamp(f"      ✅ JS Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                                        button_found = True
                                        break
                                        
                        except Exception as e:
                            continue
                            
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ TEK butonu bulunamadı!")
            
        return button_found
        
    def find_and_click_cift_button(self):
        """ÇİFT butonunu bul ve rastgele sayıda tıkla"""
        click_count = random.randint(random_min, random_max)
        log_with_timestamp(f"🎯 {self.cift_button['numara']} numaralı '{self.cift_button['text']}' butonu aranıyor...")
        log_with_timestamp(f"🎲 Rastgele tıklama sayısı: {click_count}")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"div.spin2win-box__market-display:contains('{self.cift_button['text']}')",
            f"div[class*='spin2win-box__market-display']",
            f"*:contains('{self.cift_button['text']}')",
            "div.spin2win-box__market-display"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                if ":contains" in selector:
                    # JavaScript ile contains kullan
                    elements = self.driver.execute_script(f"""
                        return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                            el => el.textContent.trim() === '{self.cift_button['text']}'
                        );
                    """)
                    
                    if elements and len(elements) > 0:
                        element = elements[0]
                        log_with_timestamp(f"   ✅ JavaScript ile '{self.cift_button['text']}' butonu bulundu!")
                        
                        # Element bilgilerini göster
                        text = self.driver.execute_script("return arguments[0].textContent.trim();", element)
                        class_name = self.driver.execute_script("return arguments[0].className;", element)
                        location = self.driver.execute_script("return {x: arguments[0].getBoundingClientRect().left, y: arguments[0].getBoundingClientRect().top};", element)
                        
                        log_with_timestamp(f"   📊 Buton Bilgileri:")
                        log_with_timestamp(f"      Text: {text}")
                        log_with_timestamp(f"      Class: {class_name}")
                        log_with_timestamp(f"      Konum: x={int(location['x'])}, y={int(location['y'])}")
                        
                        # Çoklu tıklama işlemi
                        log_with_timestamp(f"   🖱️ '{self.cift_button['text']}' butonuna {click_count} kez tıklanıyor...")
                        
                        try:
                            # JavaScript ile çoklu tıkla
                            for i in range(click_count):
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                            log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                            button_found = True
                            break
                            
                        except Exception as click_error:
                            log_with_timestamp(f"   ❌ Tıklama hatası: {str(click_error)}")
                            
                else:
                    # Normal CSS selector
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text == self.cift_button['text']:
                                    log_with_timestamp(f"   ✅ '{self.cift_button['text']}' butonu bulundu!")
                                    
                                    # Element bilgilerini göster
                                    class_name = element.get_attribute('class')
                                    location = element.location
                                    
                                    log_with_timestamp(f"   📊 Buton Bilgileri:")
                                    log_with_timestamp(f"      Text: {text}")
                                    log_with_timestamp(f"      Class: {class_name}")
                                    log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                                    
                                    # Çoklu tıklama işlemi
                                    log_with_timestamp(f"   🖱️ '{self.cift_button['text']}' butonuna {click_count} kez tıklanıyor...")
                                    
                                    try:
                                        for i in range(click_count):
                                            element.click()
                                            log_with_timestamp(f"      ✅ Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} normal tıklama başarılı!")
                                        button_found = True
                                        break
                                        
                                    except:
                                        # JavaScript ile çoklu tıkla
                                        for i in range(click_count):
                                            self.driver.execute_script("arguments[0].click();", element)
                                            log_with_timestamp(f"      ✅ JS Tıklama {i+1}/{click_count} başarılı!")
                                            time.sleep(0.1)  # Tıklamalar arası kısa bekleme
                                        log_with_timestamp(f"   ✅ Toplam {click_count} JavaScript tıklaması başarılı!")
                                        button_found = True
                                        break
                                        
                        except Exception as e:
                            continue
                            
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ '{self.cift_button['text']}' butonu bulunamadı!")
            
        return button_found
        
    def find_and_click_play_button(self):
        """OYNA butonunu bul ve tıkla"""
        log_with_timestamp(f"\n🎯 {self.play_button['numara']} numaralı 'OYNA' butonu aranıyor...")
        
        # Farklı selector'lar ile dene
        selectors_to_try = [
            f"#{self.play_button['id']}",  # ID ile
            f"div[id='{self.play_button['id']}']",
            "div.casino-game-play-button",
            "*[class*='casino-game-play-button']",
            "*[class*='play-button']",
            "*[class*='icon-play']"
        ]
        
        button_found = False
        
        for selector in selectors_to_try:
            try:
                log_with_timestamp(f"   🔍 Selector deneniyor: {selector}")
                
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    try:
                        if element.is_displayed():
                            log_with_timestamp(f"   ✅ OYNA butonu bulundu!")
                            
                            # Element bilgilerini göster
                            class_name = element.get_attribute('class')
                            id_attr = element.get_attribute('id')
                            location = element.location
                            text = element.text.strip() if element.text else 'Boş'
                            
                            log_with_timestamp(f"   📊 Buton Bilgileri:")
                            log_with_timestamp(f"      Text: {text}")
                            log_with_timestamp(f"      Class: {class_name}")
                            log_with_timestamp(f"      ID: {id_attr}")
                            log_with_timestamp(f"      Konum: x={location['x']}, y={location['y']}")
                            
                            # Tıklama işlemi
                            log_with_timestamp(f"   🖱️ OYNA butonuna tıklanıyor...")
                            
                            try:
                                element.click()
                                log_with_timestamp(f"   ✅ Normal tıklama başarılı!")
                                button_found = True
                                break
                                
                            except:
                                # JavaScript ile tıkla
                                self.driver.execute_script("arguments[0].click();", element)
                                log_with_timestamp(f"   ✅ JavaScript tıklaması başarılı!")
                                button_found = True
                                break
                                
                    except Exception as e:
                        continue
                        
                if button_found:
                    break
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ Selector hatası: {str(e)}")
                continue
                
        if not button_found:
            log_with_timestamp(f"   ❌ OYNA butonu bulunamadı!")
            
        return button_found
        
    def wait_for_game_completion(self):
        """Oyun tamamlanana kadar bekle (iframe'in kaybolması)"""
        log_with_timestamp("\n⏳ Oyun tamamlanması bekleniyor...")
        log_with_timestamp("   🔍 İframe kontrolü yapılıyor...")
        
        max_wait_time = 27  # Maksimum 60 saniye bekle
        wait_count = 0
        
        while wait_count < max_wait_time:
            try:
                # Ana sayfaya dön
                self.driver.switch_to.default_content()
                
                # İframe'leri kontrol et
                frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                
                if len(frames) == 0:
                    log_with_timestamp("   ✅ İframe kayboldu - Oyun tamamlandı!")
                    return True
                else:
                    log_with_timestamp(f"   ⏳İşlemler devam ediyor... ({wait_count + 1}/27)")
                    time.sleep(1)
                    wait_count += 1
                    
            except Exception as e:
                log_with_timestamp(f"   ❌ İframe kontrol hatası: {str(e)}")
                time.sleep(1)
                wait_count += 1
                
        return False
        
    def infinite_betting_loop(self):
        """Sonsuz TEK+ÇİFT döngüsü"""
        log_with_timestamp("\n🔄 SONSUZ BAHIS DÖNGÜSÜ BAŞLATILIYOR")
        log_with_timestamp("="*50)
        log_with_timestamp("💡 Döngü: TEK + ÇİFT → PLAY → Bekle → TEK + ÇİFT → PLAY → Bekle → ...")
        log_with_timestamp("🛑 Durdurmak için Ctrl+C basın")
        
        round_count = 1
        
        try:
            while True:
                log_with_timestamp(f"\n🎯 ROUND {round_count} - TEK + ÇİFT BAHSI")
                log_with_timestamp("-" * 50)
                
                # Frame'e geç
                self.switch_to_game_frame()
                
                # 1. TEK butonuna tıkla
                log_with_timestamp("\n🎯 1. ADIM: TEK BUTONUNA TIKLAMA")
                tek_success = self.find_and_click_tek_button()
                
                if tek_success:
                    log_with_timestamp("✅ TEK butonuna tıklama başarılı!")
                    time.sleep(1)
                    
                    # 2. ÇİFT butonuna tıkla
                    log_with_timestamp("\n🎯 2. ADIM: ÇİFT BUTONUNA TIKLAMA")
                    cift_success = self.find_and_click_cift_button()
                    
                    if cift_success:
                        log_with_timestamp("✅ ÇİFT butonuna tıklama başarılı!")
                        time.sleep(1)
                        
                        # 3. PLAY butonuna tıkla
                        log_with_timestamp("\n🎯 3. ADIM: PLAY BUTONUNA TIKLAMA")
                        play_success = self.find_and_click_play_button()
                        
                        if play_success:
                            log_with_timestamp("✅ PLAY butonuna tıklama başarılı!")
                            log_with_timestamp(f"\n🎉 ROUND {round_count} BAŞARILI!")
                            log_with_timestamp("   ✅ TEK butonuna tıklandı")
                            log_with_timestamp("   ✅ ÇİFT butonuna tıklandı")
                            log_with_timestamp("   ✅ PLAY butonuna tıklandı")
                            
                            # Oyun tamamlanana kadar bekle
                            self.wait_for_game_completion()
                            
                            round_count += 1
                            log_with_timestamp(f"🔄 Sonraki round hazırlanıyor...")
                            time.sleep(2)  # Sonraki round için kısa bekleme
                            
                        else:
                            log_with_timestamp(f"❌ PLAY butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                            time.sleep(5)
                            
                    else:
                        log_with_timestamp(f"❌ ÇİFT butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                        time.sleep(5)
                        
                else:
                    log_with_timestamp(f"❌ TEK butonuna tıklanamadı! 5 saniye bekleyip tekrar denenecek...")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            log_with_timestamp("\n\n🛑 KULLANICI TARAFINDAN DURDURULDU")
            log_with_timestamp(f"📊 Toplam {round_count - 1} round tamamlandı")
            
        except Exception as e:
            log_with_timestamp(f"\n❌ Döngü hatası: {str(e)}")
            log_with_timestamp("5 saniye bekleyip tekrar denenecek...")
            time.sleep(5)
    
    def run(self):
        """Ana çalıştırma fonksiyonu"""
        try:
            log_with_timestamp("🎰 SONSUZ TEK+ÇİFT BAHIS SİSTEMİ")
            log_with_timestamp("="*50)
            
            # WebDriver'ı başlat
            self.setup_driver()
            
            # Sayfayı yükle
            self.load_page()
            
            # Sonsuz döngüyü başlat
            self.infinite_betting_loop()
                
        except Exception as e:
            log_with_timestamp(f"❌ Hata oluştu: {str(e)}")
            
        finally:
            if self.driver:
                log_with_timestamp("\n🔒 Tarayıcı kapatılıyor...")
                time.sleep(2)
                self.driver.quit()
                log_with_timestamp("✅ İşlem tamamlandı!")

def main():
    clicker = BahisButtonClicker()
    clicker.run()

if __name__ == "__main__":
    main()
