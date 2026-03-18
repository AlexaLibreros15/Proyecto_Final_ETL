# Pipeline ETL — Publicidad Digital

> Universidad Autónoma de Occidente — Maestría en Generación de IA y Data Science
> Asignatura: ETL (Extracción, Transformación y Carga) — 2026-1S

## Descripción

Pipeline ETL automatizado que consolida datos de campañas publicitarias digitales de múltiples plataformas en una **Master Table** unificada para análisis de rendimiento.

**Problema:** Las agencias de publicidad digital manejan datos fragmentados entre plataformas (Meta Ads, Google Ads, GA4, Search Console). Los Media Traders consolidan manualmente en Excel, perdiendo tiempo y cometiendo errores ("Excel Hell").

**Solución:** Un pipeline modular que extrae datos de 5 fuentes, estandariza formatos (fechas, tipos, taxonomías) y genera una tabla consolidada por fecha, lista para análisis y dashboards.

**Metodología:** Estructura basada en CRISP-DM, con separación de datos crudos (`data/raw/`) y procesados (`data/processed/`), código modular en `src/` y ambiente virtual aislado.

## Equipo

| Nombre | GitHub |
|--------|--------|
| Christian Felipe Trujillo Franco | @thepipo93 |
| Juan Sebastián Hoyos Espinosa | @Jshe1113 |
| Koraima Torres | @koraimatorresd |
| Alexandra Libreros | @AlexaLibreros15 |

## Estructura del proyecto (CRISP-DM)

```
Proyecto_Final_ETL/
├── data/
│   ├── raw/                        # Datos crudos originales (anonimizados)
│   │   ├── ga4_2025.csv            # Google Analytics 4 (3,000 filas)
│   │   ├── google_ads_2025.csv     # Google Ads (1,219 filas)
│   │   ├── meta_ads_2025.csv       # Meta Ads (26 filas, mensual)
│   │   ├── gsc_chart_2025.csv      # Google Search Console - diario (335 filas)
│   │   ├── gsc_queries_2025.csv    # Google Search Console - queries (996 filas)
│   │   └── ventas_2025.csv         # Pólizas de seguros del cliente (1,011 filas)
│   └── processed/                  # Datos limpios y transformados
│       └── master_table.csv        # Tabla consolidada final (363 filas x 16 cols)
├── src/
│   ├── extract.py                  # Lectura de las 5 fuentes con pd.read_csv()
│   ├── transform.py                # Limpieza, estandarización, cálculo de KPIs y merge
│   ├── load.py                     # Exportación de master table y reporte de calidad
│   └── pipeline.py                 # Orquestador principal (E → T → L)
├── requirements.txt                # Dependencias del proyecto (pip freeze)
├── .env                            # Variables de entorno (credenciales, no subir)
├── .gitignore                      # Excluye venv/, .env, __pycache__/
└── README.md
```

## Fuentes de datos

| Fuente | Formato | Método de extracción | Filas | Descripción |
|--------|---------|---------------------|-------|-------------|
| Google Analytics 4 | CSV | BigQuery SQL | 3,000 | Sesiones, usuarios, pageviews por fuente/medio/campaña/día |
| Google Ads | CSV | API REST v23 | 1,219 | Campañas Search/Display: impresiones, clics, costo, conversiones por día |
| Meta Ads | CSV | Graph API v22.0 | 26 | Campañas Facebook/Instagram: spend, CPM, reach, frequency, results por mes |
| Google Search Console | CSV | Descarga manual | 335 + 996 | Clics/impresiones orgánicos diarios + queries de búsqueda |
| Ventas (Pólizas) | CSV | Archivo del cliente | 1,011 | Código producto, número póliza, fecha, monto |

## Stack tecnológico

| Capa | Herramienta |
|------|-------------|
| Lenguaje | Python 3.12+ |
| Extracción | pandas (`read_csv`) |
| Transformación | pandas (`to_datetime`, `merge`, `groupby`, `fillna`, `drop_duplicates`) |
| Carga | CSV procesado (`to_csv`) |
| Orquestación | `pipeline.py` modular (funciones `def` con tuplas entre etapas) |
| Versionamiento | GitHub |
| Entorno | venv + requirements.txt |

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlexaLibreros15/Proyecto_Final_ETL.git
cd Proyecto_Final_ETL
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el pipeline

```bash
cd src
python pipeline.py
```

El resultado se guarda en `data/processed/master_table.csv`.

## Proceso ETL

### Extracción (`extract.py`)
Lee los 6 archivos CSV desde `data/raw/` usando `pd.read_csv()`. Cada fuente se carga como un DataFrame independiente y se retornan como tupla. Incluye `try/except` para manejar errores sin romper la ejecución.

### Transformación (`transform.py`)
- Estandarización de fechas a formato `YYYY-MM-DD` con `pd.to_datetime(errors='coerce')`
- Conversión de tipos con `pd.to_numeric(errors='coerce')`
- Relleno de nulos con `fillna(0)`
- Eliminación de duplicados con `drop_duplicates()`
- Cálculo de KPIs derivados: CPM, CPC, CPA
- Agregación por fecha con `groupby().agg()`
- Merge de todas las fuentes por fecha con `merge(on='fecha', how='outer')`
- Resultado: Master Table con 363 filas (1 por día de 2025) y 16 columnas

### Carga (`load.py`)
- Exporta la Master Table a `data/processed/master_table.csv` con `to_csv(index=False)`
- Genera reporte de calidad: filas, columnas, nulls y duplicados por cada fuente

## KPIs calculados

| Métrica | Fórmula | Descripción |
|---------|---------|-------------|
| CPM | (cost / impressions) * 1000 | Costo por mil impresiones |
| CPC | cost / clicks | Costo por clic |
| CPA | cost / conversions | Costo por adquisición |
| CTR | clicks / impressions | Tasa de clics (viene de las APIs) |
| Frecuencia | reach / impressions | Veces promedio que un usuario vio el anuncio (Meta) |

## Master Table (`data/processed/master_table.csv`)

363 filas (una por día calendario de 2025), 16 columnas:

| Columna | Fuente | Descripción |
|---------|--------|-------------|
| `fecha` | Todas | Fecha del día |
| `ga4_sesiones` | GA4 | Total sesiones en el sitio web |
| `ga4_usuarios` | GA4 | Usuarios únicos activos |
| `ga4_pageviews` | GA4 | Páginas vistas |
| `ga4_nuevos` | GA4 | Usuarios nuevos |
| `gads_impressions` | Google Ads | Impresiones de anuncios |
| `gads_clicks` | Google Ads | Clics en anuncios |
| `gads_cost` | Google Ads | Gasto en USD |
| `gads_conversions` | Google Ads | Conversiones reportadas |
| `gads_cpm` | Calculado | CPM de Google Ads |
| `gads_cpc` | Calculado | CPC de Google Ads |
| `gads_cpa` | Calculado | CPA de Google Ads |
| `gsc_clicks` | GSC | Clics orgánicos desde Google |
| `gsc_impressions` | GSC | Impresiones orgánicas |
| `ventas_cantidad` | Ventas | Pólizas emitidas ese día |
| `ventas_monto` | Ventas | Monto total de pólizas |

## Nota sobre atribución

El sitio web del cliente no cuenta con página de confirmación (thank-you page). La relación entre gasto publicitario y ventas de pólizas es únicamente **temporal** (correlación por fecha), no de atribución directa. Este gap es un hallazgo del proyecto y la recomendación para 2026 es implementar un flujo de conversión trackeable.
