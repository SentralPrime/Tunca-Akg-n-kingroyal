# Railway için minimal ve güvenilir Dockerfile
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

# ChromeDriver yükle
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

# Çalışma dizini
WORKDIR /app

# Python requirements yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Railway environment variables
ENV RAILWAY_ENVIRONMENT=production
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV PORT=8080

# Port expose et
EXPOSE 8080

# Uygulama başlat
CMD ["python", "app.py"] 