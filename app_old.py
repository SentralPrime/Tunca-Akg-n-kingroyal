from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
import json
from datetime import datetime
import sys
import os
from io import StringIO
import contextlib
import random
from selenium.webdriver.common.by import By
from deneme1 import BahisButtonClicker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'casino_bot_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global değişkenler
bot_instance = None
bot_thread = None
bot_running = False
round_count = 0
terminal_output = []
account_owner = "Ömer Gezer"

class TerminalCapture:
    def __init__(self):
        self.output = StringIO()
        
    def write(self, message):
        # Hem socketio'ya hem de terminal'e yazdır
        if message.strip():
            terminal_output.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': message.strip()
            })
            # Son 100 çıktıyı tut
            if len(terminal_output) > 100:
                terminal_output.pop(0)
            
            # WebSocket ile gönder
            socketio.emit('terminal_output', {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': message.strip()
            })
        
        # Orijinal stdout'a da yazdır
        sys.__stdout__.write(message)
        sys.__stdout__.flush()
        
    def flush(self):
        pass

# Terminal çıktısını yakala
terminal_capture = TerminalCapture()

def custom_log_with_timestamp(message):
    """Custom log function that captures output"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Terminal çıktısını kaydet
    terminal_output.append({
        'timestamp': timestamp,
        'message': message
    })
    
    # Son 100 çıktıyı tut
    if len(terminal_output) > 100:
        terminal_output.pop(0)
    
    # Console'a da yazdır
    print(formatted_message)
    sys.stdout.flush()
    
    # WebSocket ile gönder - Polling yerine direkt emit
    try:
        socketio.emit('terminal_output', {
            'timestamp': timestamp,
            'message': message
        }, broadcast=True)
    except:
        pass

def run_bot():
    """Bot çalıştırma fonksiyonu - Basitleştirilmiş çıktı"""
    global bot_instance, bot_running, round_count
    
    # Flask-SocketIO background task olarak çalıştırılacak
    with app.app_context():
        try:
        custom_log_with_timestamp("🎰 Bot başlatılıyor...")
        bot_instance = BahisButtonClicker()
        
        # WebDriver'ı başlat
        bot_instance.setup_driver()
        
        # Sayfayı yükle - 15 saniye bekleme bildirimi
        custom_log_with_timestamp("⏳ 15 saniye bekleme süresi başladı...")
        bot_instance.load_page()
        custom_log_with_timestamp("✅ Sayfa yüklendi, bot hazır!")
        
        # Sonsuz döngü - round sayacını takip et
        round_count = 1
        
        while bot_running:
            try:
                custom_log_with_timestamp(f"🎯 ROUND {round_count} başlıyor...")
                
                # Frame'e geç
                bot_instance.switch_to_game_frame()
                
                # 1. TEK butonuna tıkla - rastgele sayıda
                tek_click_count = random.randint(1, 6)
                tek_success = custom_click_tek_button(bot_instance, tek_click_count)
                
                if tek_success and bot_running:
                    custom_log_with_timestamp(f"✅ TEK butonuna ({tek_click_count}) defa basıldı")
                    time.sleep(1)
                    
                    # 2. ÇİFT butonuna tıkla - rastgele sayıda
                    cift_click_count = random.randint(1, 6)
                    cift_success = custom_click_cift_button(bot_instance, cift_click_count)
                    
                    if cift_success and bot_running:
                        custom_log_with_timestamp(f"✅ ÇİFT butonuna ({cift_click_count}) defa basıldı")
                        time.sleep(1)
                        
                        # 3. PLAY butonuna tıkla
                        play_success = custom_click_play_button(bot_instance)
                        
                        if play_success and bot_running:
                            custom_log_with_timestamp("✅ PLAY butonuna basıldı, işlemlerin bitmesi bekleniyor (27 saniye)...")
                            
                            # Round sayısını güncelle
                            def emit_round_update():
                                socketio.emit('round_update', {'round': round_count})
                            socketio.start_background_task(emit_round_update)
                            
                            # 27 saniye bekle
                            custom_wait_for_completion()
                            
                            round_count += 1
                            custom_log_with_timestamp(f"🎉 ROUND {round_count-1} tamamlandı! Sonraki round hazırlanıyor...")
                            time.sleep(3)
                            
                        else:
                            custom_log_with_timestamp("❌ PLAY butonuna basılamadı! Tekrar deneniyor...")
                            time.sleep(5)
                            
                    else:
                        custom_log_with_timestamp("❌ ÇİFT butonuna basılamadı! Tekrar deneniyor...")
                        time.sleep(5)
                        
                else:
                    custom_log_with_timestamp("❌ TEK butonuna basılamadı! Tekrar deneniyor...")
                    time.sleep(5)
                    
            except Exception as e:
                custom_log_with_timestamp(f"❌ Hata oluştu: {str(e)}")
                time.sleep(5)
                
    except Exception as e:
        custom_log_with_timestamp(f"❌ Bot hatası: {str(e)}")
        
    finally:
        if bot_instance and bot_instance.driver:
            custom_log_with_timestamp("🔒 Tarayıcı kapatılıyor...")
            bot_instance.driver.quit()
            custom_log_with_timestamp("✅ Bot durduruldu!")

def custom_click_tek_button(bot_instance, click_count):
    """TEK butonuna basma - basitleştirilmiş"""
    try:
        bot_instance.switch_to_game_frame()
        elements = bot_instance.driver.execute_script("""
            return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                el => el.textContent.trim() === 'TEK'
            );
        """)
        
        if elements and len(elements) > 0:
            element = elements[0]
            for i in range(click_count):
                bot_instance.driver.execute_script("arguments[0].click();", element)
                time.sleep(0.1)
            return True
    except:
        pass
    return False

def custom_click_cift_button(bot_instance, click_count):
    """ÇİFT butonuna basma - basitleştirilmiş"""
    try:
        bot_instance.switch_to_game_frame()
        elements = bot_instance.driver.execute_script("""
            return Array.from(document.querySelectorAll('div.spin2win-box__market-display')).filter(
                el => el.textContent.trim() === 'ÇİFT'
            );
        """)
        
        if elements and len(elements) > 0:
            element = elements[0]
            for i in range(click_count):
                bot_instance.driver.execute_script("arguments[0].click();", element)
                time.sleep(0.1)
            return True
    except:
        pass
    return False

def custom_click_play_button(bot_instance):
    """PLAY butonuna basma - basitleştirilmiş"""
    try:
        bot_instance.switch_to_game_frame()
        element = bot_instance.driver.find_element(By.ID, "game-play-button")
        if element.is_displayed():
            bot_instance.driver.execute_script("arguments[0].click();", element)
            return True
    except:
        pass
    return False

def custom_wait_for_completion():
    """27 saniye bekleme"""
    for i in range(27):
        if not bot_running:
            break
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html', account_owner=account_owner)

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_thread, bot_running
    
    if not bot_running:
        bot_running = True
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Bot başlatıldı!',
            'running': True
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Bot zaten çalışıyor!',
            'running': True
        })

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global bot_running
    
    if bot_running:
        bot_running = False
        custom_log_with_timestamp("🛑 Bot durdurma komutu verildi...")
        
        return jsonify({
            'status': 'success',
            'message': 'Bot durduruldu!',
            'running': False
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Bot zaten durmuş!',
            'running': False
        })

@app.route('/status')
def status():
    return jsonify({
        'running': bot_running,
        'round': round_count,
        'account_owner': account_owner
    })

@app.route('/logs')
def logs():
    return jsonify(terminal_output)

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Bağlantı başarılı!'})
    emit('round_update', {'round': round_count})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 