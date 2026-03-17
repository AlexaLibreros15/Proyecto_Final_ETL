"""
extract.py — Modulo de Extraccion
Proyecto Final ETL — Maestria en IA y Ciencia de Datos (UAO)

Lee las 5 fuentes de datos desde data/raw/ y retorna DataFrames validados.
"""
import pandas as pd
import os

DATA_RAW = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


def extract_ga4():
    """Extrae datos de Google Analytics 4 (exportados via BigQuery)."""
    path = os.path.join(DATA_RAW, 'ga4_2025.csv')
    df = pd.read_csv(path, dtype={'fecha': str})
    print(f"[EXTRACT] GA4: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def extract_google_ads():
    """Extrae datos de Google Ads (exportados via API REST)."""
    path = os.path.join(DATA_RAW, 'google_ads_2025.csv')
    df = pd.read_csv(path)
    print(f"[EXTRACT] Google Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def extract_meta_ads():
    """Extrae datos de Meta Ads (exportados via Graph API)."""
    path = os.path.join(DATA_RAW, 'meta_ads_2025.csv')
    df = pd.read_csv(path)
    print(f"[EXTRACT] Meta Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def extract_gsc():
    """Extrae datos de Google Search Console (Chart diario + Queries)."""
    chart_path = os.path.join(DATA_RAW, 'gsc_chart_2025.csv')
    queries_path = os.path.join(DATA_RAW, 'gsc_queries_2025.csv')
    df_chart = pd.read_csv(chart_path)
    df_queries = pd.read_csv(queries_path)
    print(f"[EXTRACT] GSC Chart: {df_chart.shape[0]} filas | Queries: {df_queries.shape[0]} filas")
    return df_chart, df_queries


def extract_ventas():
    """Extrae datos de ventas/polizas (CSV interno del cliente)."""
    path = os.path.join(DATA_RAW, 'ventas_2025.csv')
    df = pd.read_csv(path)
    print(f"[EXTRACT] Ventas: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def extract_all():
    """Ejecuta toda la extraccion y retorna un diccionario de DataFrames."""
    print("=" * 60)
    print("ETAPA: EXTRACCION")
    print("=" * 60)
    ga4 = extract_ga4()
    gads = extract_google_ads()
    meta = extract_meta_ads()
    gsc_chart, gsc_queries = extract_gsc()
    ventas = extract_ventas()
    print(f"\n[EXTRACT] Extraccion completa: 5 fuentes cargadas")
    return {
        'ga4': ga4,
        'google_ads': gads,
        'meta_ads': meta,
        'gsc_chart': gsc_chart,
        'gsc_queries': gsc_queries,
        'ventas': ventas
    }


if __name__ == '__main__':
    data = extract_all()
    for name, df in data.items():
        print(f"  {name}: {df.shape}")
