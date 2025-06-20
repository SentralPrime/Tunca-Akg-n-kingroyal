# Railway Memory Optimized Dockerfile
FROM python:3.11-slim

# Sistem kullanıcısı oluştur
RUN useradd --create-home --shell /bin/bash app

# Railway için shared memory artır
RUN echo 'kernel.shmmax = 134217728' >> /etc/sysctl.conf

# Sistem bağımlılıklarını yükle - minimal set
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    ca-certificates \
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
    libgbm1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Google Chrome repository ve key ekle  
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Google Chrome yükle
RUN apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# ChromeDriver'ı yükle - sabit versiyon
RUN wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

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
ENV RAILWAY_ENVIRONMENT=production
ENV DISPLAY=:99
ENV PORT=8080
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Railway memory ayarları
ENV MALLOC_ARENA_MAX=2
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV MALLOC_TRIM_THRESHOLD_=131072
ENV MALLOC_TOP_PAD_=131072
ENV MALLOC_MMAP_MAX_=65536

# Port ayarla
EXPOSE 8080

# Shared memory mount point oluştur
RUN mkdir -p /dev/shm && chmod 1777 /dev/shm

# app kullanıcısına geç
USER app

# Flask uygulamasını başlat
CMD ["python", "app.py"] 