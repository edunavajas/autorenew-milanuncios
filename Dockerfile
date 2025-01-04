FROM python:3.10-slim

# Actualizar claves GPG
RUN apt-get update && apt-get install -y --no-install-recommends gnupg && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9 6ED0E7B82643E131 F8D2585B8783D481 54404762BBB6E853 BDE6D2B9216EC7A8 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget libnss3 libxss1 libasound2 libatk1.0-0 libcups2 libdbus-1-3 libxcomposite1 \
    libxrandr2 libxdamage1 libpangocairo-1.0-0 libgtk-3-0 libgbm1 libpango-1.0-0 libcairo2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Playwright
RUN pip install --no-cache-dir playwright

# Instalar navegadores Playwright
RUN playwright install

# Copiar el script al contenedor
WORKDIR /app
COPY init.py /app

# Comando por defecto
CMD ["python", "init.py"]
