# First-dag
Un dag pour exporter des images plotly
```powershell
#.0 --------IMPORTANT DELETE RESSSOURCES--------->
docker-compose down --volumes --rmi all
# Créer le fichier .env avec les bons encodages
Remove-Item -ErrorAction Ignore .env
Set-Content -Path .env -Value "AIRFLOW_UID=50000" -Encoding Ascii

# 1. Télécharger le fichier docker-compose officiel stable
curl.exe -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

# dans le docker-compose.yaml
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

```powershell
# 2. Créer les dossiers locaux nécessaires
mkdir -Force dags, logs, plugins, data

# Préparer et initialiser la base de données (Metastore)
docker-compose up airflow-init

# lancer Airflow et lancer la reconstruction de l'image
docker-compose up -d --build

```
lancer l'airflow UI
http://localhost:8080/
