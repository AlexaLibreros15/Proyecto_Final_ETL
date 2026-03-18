# Pipeline ETL — Publicidad Digital

> Universidad Autónoma de Occidente — Maestría en Generación de IA y Data Science
> Asignatura: ETL (Extracción, Transformación y Carga) — 2026-1S

## Descripción

Pipeline ETL automatizado que consolida datos de campañas publicitarias digitales de múltiples plataformas en una **Master Table** unificada para análisis de rendimiento.

**Problema:** Las agencias de publicidad digital manejan datos fragmentados entre plataformas (Meta Ads, Google Ads, GA4, Search Console). Los Media Traders consolidan manualmente en Excel, perdiendo tiempo y cometiendo errores.

**Solución:** Un pipeline que extrae datos de 5 fuentes, estandariza formatos (fechas, monedas, taxonomías) y genera una tabla consolidada lista para análisis y dashboards.

## Equipo

| Nombre | GitHub |
|--------|--------|
| Christian Felipe Trujillo Franco | @cristiantru |
| Juan Sebastián Hoyos Espinosa | @jshe1113 |
| Koraima Torres | @koraimatorresd |
| Alexandra Libreros | @AlexaLibreros15 |

## Estructura del proyecto

```
Proyecto_Final_ETL/
├── data/
│   ├── raw/                    # Datos crudos (CSVs y Excel descargados)
│   │   ├── ga4_2025.csv        # Google Analytics 4
│   │   ├── gsc_2025.csv        # Google Search Console
│   │   ├── meta_ads_2025.csv   # Meta Ads (Facebook/Instagram)
│   │   ├── google_ads_2025.csv # Google Ads
│   │   └── ventas_2025.xlsx    # Pólizas de seguros del cliente
│   └── processed/              # Datos limpios y transformados
│       └── master_table.csv    # Tabla consolidada final
├── src/
│   ├── extract.py              # Lectura de datos desde archivos planos
│   ├── transform.py            # Limpieza, estandarización y merge
│   ├── load.py                 # Exportación de la master table
│   └── pipeline.py             # Orquestador principal (E → T → L)
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Variables de entorno (no subir a GitHub)
├── .gitignore
└── README.md
```

## Fuentes de datos

| Fuente | Formato | Descripción |
|--------|---------|-------------|
| Google Analytics 4 | CSV | Sesiones, usuarios, bounce rate, fuentes de tráfico |
| Google Search Console | CSV | Queries orgánicas, clics, impresiones, posición |
| Meta Ads | CSV | Campañas Facebook/Instagram: impresiones, clics, gasto, CPM |
| Google Ads | CSV | Campañas Search/Display: impresiones, clics, costo, conversiones |
| Ventas (Pólizas) | XLSX | Registro interno: código producto, fecha, monto |

## Stack tecnológico

| Capa | Herramienta |
|------|-------------|
| Lenguaje | Python 3.12+ |
| Extracción | pandas (read_csv, read_excel) |
| Transformación | Pandas + NumPy |
| Carga | CSV procesado (BigQuery opcional) |
| Orquestación | pipeline.py modular |
| Versionamiento | GitHub |
| Entorno | VS Code + venv |

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlexaLibreros15/Proyecto_Final_ETL.git
cd Proyecto_Final_ETL
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar el entorno:

- **Windows:**
```bash
venv\Scripts\activate
```
- **Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Colocar los datos

Descargar los archivos de cada plataforma y colocarlos en `data/raw/`:

- `ga4_2025.csv` → desde Google Analytics 4 (Explorar → Exportar)
- `gsc_2025.csv` → desde Google Search Console (Rendimiento → Exportar)
- `meta_ads_2025.csv` → desde Meta Ads Manager (Reportes → Exportar)
- `google_ads_2025.csv` → desde Google Ads (Informes → Descargar)
- `ventas_2025.xlsx` → proporcionado por el cliente

### 5. Ejecutar el pipeline

```bash
python src/pipeline.py
```

El resultado se guarda en `data/processed/master_table.csv`.

## Proceso ETL

### Extracción
Lee los 5 archivos desde `data/raw/` usando `pandas.read_csv()` y `pandas.read_excel()`. Cada fuente se carga como un DataFrame independiente.

### Transformación
- Estandarización de fechas a formato `YYYY-MM-DD`
- Limpieza de moneda (USD/GTQ) a valores numéricos
- Renombrado de columnas a esquema común entre plataformas
- Eliminación de filas basura (headers extra en Google Ads)
- Cálculo de KPIs: CPM, CPC, CTR
- Eliminación de duplicados y valores nulos
- Merge temporal por fecha para cruzar todas las fuentes

### Carga
Exporta la Master Table consolidada a `data/processed/master_table.csv`, lista para conectar con Looker Studio, Streamlit o cualquier herramienta de visualización.

## KPIs del proyecto

| Métrica | Descripción |
|---------|-------------|
| CPM | Costo por mil impresiones |
| CPC | Costo por clic |
| CPA | Costo por adquisición |
| CTR | Tasa de clics |
| ROAS | Retorno sobre inversión publicitaria |
| Frecuencia | Veces promedio que un usuario vio el anuncio |

## Nota sobre atribución

El sitio web del cliente no cuenta con página de confirmación (thank-you page) ni carrito de compras. Por lo tanto, la relación entre gasto publicitario y ventas de pólizas es únicamente **temporal** (por fecha), no de atribución directa.
