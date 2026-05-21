# First-dag
Un dag pour exporter des images plotly
## powershell
```powershell
#.0 --------IMPORTANT DELETE RESSSOURCES--------->
docker-compose down --volumes --rmi all
# Créer le fichier .env avec les bons encodages
Remove-Item -ErrorAction Ignore .env
Set-Content -Path .env -Value "AIRFLOW_UID=50000" -Encoding Ascii

# 1. Télécharger le fichier docker-compose officiel stable
curl.exe -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

## dans le docker-compose.yaml
```yaml
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.2.1}
  build: .   #décommenter

#   volumes:
  - ./dags:/opt/airflow/dags
  - ./logs:/opt/airflow/logs
  - ./config:/opt/airflow/config
  - ./plugins:/opt/airflow/plugins
  - ./data:/opt/airflow/data

# virer les dags exemples
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```

## powershell
```powershell
# 2. Créer les dossiers locaux nécessaires
mkdir -Force dags, logs, plugins, data

# Préparer et initialiser la base de données (Metastore)
docker-compose up airflow-init

# lancer Airflow et lancer la reconstruction de l'image
docker-compose up -d --build
```
### Dockerfile pour générer les images avec plotly (engine = 'orca')
```
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
```


```
# si pb
docker-compose down

# re build
docker-compose up -d --build --d

```


lancer l'airflow UI
http://localhost:8080/
