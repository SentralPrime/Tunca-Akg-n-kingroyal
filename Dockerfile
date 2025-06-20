# Railway için optimize edilmiş Dockerfile
FROM python:3.11-slim

# Sistem kullanıcısı oluştur (güvenlik için)
RUN useradd --create-home --shell /bin/bash app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    libgbm1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome repository ve key ekle
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Google Chrome yükle
RUN apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# ChromeDriver'ı yükle (uyumlu versiyon)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1-3) \
    && echo "Chrome version: $CHROME_VERSION" \
    && wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])")/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Chrome binary'nin yerini kontrol et
RUN which google-chrome || which google-chrome-stable || which chromium-browser

# Çalışma dizini oluştur
WORKDIR /app

# Sahipliği değiştir
RUN chown -R app:app /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Railway ortam değişkenlerini ayarla
ENV RAILWAY_ENVIRONMENT=true
ENV DISPLAY=:99
ENV PORT=8080
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Port ayarla (Railway için)
EXPOSE 8080

# app kullanıcısına geç
USER app

# Flask uygulamasını başlat
CMD ["python", "app.py"] 