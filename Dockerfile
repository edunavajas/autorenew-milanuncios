FROM arm32v7/python:3.10-slim

# Actualizar repositorios y paquetes esenciales
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg libnss3 libxss1 libasound2 libatk1.0-0 libcups2 libdbus-1-3 libxcomposite1 \
    libxrandr2 libxdamage1 libpangocairo-1.0-0 libgtk-3-0 libgbm1 libpango-1.0-0 libcairo2 \
    python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Playwright
RUN pip3 install --no-cache-dir playwright

# Instalar navegadores de Playwright
RUN playwright install-deps && playwright install

# Crear directorio de trabajo
WORKDIR /app

# Copiar el script
COPY init.py /app

# Configuración de entrada
CMD ["python3", "init.py"]
