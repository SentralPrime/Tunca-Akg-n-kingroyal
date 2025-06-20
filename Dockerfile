# Render.com için minimal çalışan Dockerfile
FROM python:3.11-slim-bullseye

# Root olarak devam et
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

# Chrome ve working dependencies yükle (libindicator7 kaldırıldı)
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    libnss3 \
    libxss1 \
    libgconf-2-4 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver yükle - Chrome 137 ile uyumlu versiyon
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | sed 's/\.[^.]*$//') && \
    echo "Chrome version detected: $CHROME_VERSION" && \
    wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 && \
    echo "ChromeDriver version:" && \
    chromedriver --version

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

# Port expose et
EXPOSE 10000

# Uygulama başlat
CMD ["python", "app.py"] 