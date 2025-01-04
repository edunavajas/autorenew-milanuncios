FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y wget libnss3 libxss1 libasound2 libatk1.0-0 libcups2 libdbus-1-3 libxcomposite1 libxrandr2 libxdamage1 libpangocairo-1.0-0 libgtk-3-0 libgbm1 libpango-1.0-0 libcairo2

# Instalar Playwright
RUN pip install --no-cache-dir playwright

# Instalar navegadores Playwright
RUN playwright install

# Copiar el script al contenedor
WORKDIR /app
COPY init.py /app

# Comando por defecto
CMD ["python", "init.py"]
