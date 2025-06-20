# Render.com için optimize edilmiş Dockerfile
FROM python:3.11-slim-bullseye

# Root olarak kalan işlemleri yap
USER root

# Update sources ve temel bağımlılıkları yükle
RUN apt-get update --fix-missing && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome signing key ve repository ekle
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Chrome ve minimal dependencies yükle
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver yükle - Render için sabit versiyon
RUN wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.69/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Çalışma dizini
WORKDIR /app

# Python requirements yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Render environment variables
ENV RENDER_ENVIRONMENT=true
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV PORT=10000

# Port expose et (Render için 10000)
EXPOSE 10000

# Uygulama başlat
CMD ["python", "app.py"] 