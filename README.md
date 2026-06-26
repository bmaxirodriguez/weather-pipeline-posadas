\# 🌦️ Pipeline de Monitoreo Climático y Alertas End-to-End



Este proyecto implementa un pipeline de datos (ETL) completo utilizando la \*\*Arquitectura Medallón\*\* para recopilar, limpiar, transformar y analizar datos meteorológicos en tiempo real de la ciudad de \*\*Posadas, Misiones\*\*. El objetivo final es generar alertas automatizadas ante eventos climáticos extremos (olas de calor, frío intenso o tormentas fuertes).



\## 🏛️ Arquitectura del Proyecto



El proyecto emula un entorno de forma local utilizando \*\*DuckDB\*\* como motor de procesamiento analítico y \*\*Parquet\*\* como formato de almacenamiento eficiente (columnar y comprimido).



El proceso de ETL sigue la arquitectura Medallón:


1\. \*\*Bronze (Raw data):\*\* Ingesta de datos en formato JSON desde la API pública de \*\*Open-Meteo\*\*. El dato se conserva sin modificaciones en archivos Parquet, añadiendo únicamente metadatos de control (`ingested\_at`) para garantizar la trazabilidad.

2\. \*\*Silver (Clean data):\*\* Procesamiento con DuckDB para normalizar nombres de columnas a \*snake\_case\*, validación y casteo de tipos de datos (`TIMESTAMP`, `FLOAT`, `INT`), y filtrado de registros nulos.

3\. \*\*Gold (Business data):\*\* Agregación de datos y aplicación de reglas de negocio para clasificar alertas meteorológicas según umbrales de la región:

&#x20;  \* 🔴 \*\*Calor Extremo:\*\* Temperatura ≥ 38.0 °C

&#x20;  \* 🔵 \*\*Frío Intenso:\*\* Temperatura ≤ 8.0 °C

&#x20;  \* 🌧️ \*\*Lluvia Fuerte / Tormenta:\*\* Precipitación ≥ 15.0 mm en una hora

&#x20;  \* Adicionalmente, se genera un resumen diario de KPIs (máximas, mínimas, promedios) para optimizar el consumo de la capa analítica.



\## 🛠️ Tecnologías y Herramientas



\* \*\*Lenguaje:\*\* Python

\* \*\*Procesamiento y Base de Datos:\*\* DuckDB (SQL) \& Pandas

\* \*\*Formatos de Almacenamiento:\*\* Parquet \& PyArrow

\* \*\*Visualización / Frontend:\*\* Streamlit \& Folium (Mapas Interactivos)

\* \*\*Entorno de Desarrollo:\*\* Jupyter Notebooks \& Terminal Anaconda



\## 📁 Estructura del Repositorio



```text

├── Data/                  # Excluida en .gitignore (Almacenamiento Local)

│   ├── bronze/            # Parquet crudos por fecha/hora

│   ├── silver/            # Parquet unificado y limpio

│   └── gold/              # Tablas de alertas y resúmenes listos para consumo

├── notebooks/

│   ├── 1\_ingesta\_bronze.ipynb       # Extracción de API e ingesta

│   ├── 2\_procesamiento\_silver.ipynb # Limpieza y normalización SQL

│   └── 3\_analitica\_gold.ipynb       # Lógica de alertas y KPIs

├── app.py                 # Dashboard nteractivo en Streamlit

├── requirements.txt       # Dependencias del proyecto

└── .gitignore             # Filtro de archivos para el repositorio

