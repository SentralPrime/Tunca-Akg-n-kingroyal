# 🎰 Python Bot Site - Render Deployment

Bu proje, casino oyunlarında otomatik bahis yapan bir Python bot uygulamasıdır.

## 🚀 Özellikler

- **Selenium WebDriver** ile otomatik tarayıcı kontrolü
- **Flask Web Interface** - Web tabanlı kontrol paneli
- **Real-time WebSocket** - Canlı log takibi
- **TEK/ÇİFT Bahis Sistemi** - Otomatik bahis algoritması
- **Docker Container** - Cloud deployment ready

## 🛠️ Teknolojiler

- **Python 3.11**
- **Flask + SocketIO**
- **Selenium WebDriver**
- **Chrome Headless**
- **Docker**

## 📦 Render Deployment

### Otomatik Deployment:
1. GitHub repository'yi Render'a bağla
2. "New Web Service" seç
3. Docker runtime seç
4. Deploy butonuna bas

### Manuel Deployment:
```bash
# Render CLI yükle
npm install -g @render/cli

# Deploy et
render deploy
```

## 🔧 Environment Variables

- `PORT`: Web server portu (varsayılan: 10000)
- `RENDER_ENVIRONMENT`: Render ortam tespiti
- `DISPLAY`: Headless display ayarı

## 📝 Kullanım

1. Web interface'e git: `https://your-app.onrender.com`
2. "Bot Başlat" butonuna tıkla
3. Real-time logları takip et
4. Bot durdurmak için "Bot Durdur" butonuna tıkla

## ⚠️ Notlar

- Bot Headless mode'da çalışır
- Chrome ve ChromeDriver otomatik yüklenir
- WebSocket ile real-time iletişim
- Auto-restart özelliği mevcuttur

## 📊 Monitoring

- `/status` - Bot durumu API
- `/logs` - Log çıktıları API
- WebSocket events - Real-time updates 