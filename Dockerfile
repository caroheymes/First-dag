FROM apache/airflow:3.2.1-python3.12

USER root

# 1. Dépendances système pour Orca et les faux écrans (ajout de libasound2)
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    libgtk2.0-0 \
    libgconf-2-4 \
    libxss1 \
    libnss3 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Extraction d'Orca et création du script avec APPDIR
RUN wget https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage -O /tmp/orca.AppImage \
    && chmod +x /tmp/orca.AppImage \
    && cd /tmp \
    && ./orca.AppImage --appimage-extract \
    && mv squashfs-root /opt/orca \
    && rm /tmp/orca.AppImage \
    && chmod -R 777 /opt/orca \
    && echo '#!/bin/bash' > /usr/local/bin/orca \
    && echo 'export APPDIR=/opt/orca' >> /usr/local/bin/orca \
    && echo 'exec /opt/orca/AppRun "$@"' >> /usr/local/bin/orca \
    && chmod 777 /usr/local/bin/orca

USER airflow

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
