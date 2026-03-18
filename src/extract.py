"""
extract.py — Modulo de Extraccion
Lee las 5 fuentes de datos desde data/raw/ y retorna una tupla de DataFrames.
"""
import pandas as pd
import os

DATA_RAW = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


def extraer_ga4():
    """Extrae datos de Google Analytics 4."""
    try:
        path = os.path.join(DATA_RAW, 'ga4_2025.csv')
        df = pd.read_csv(path, dtype={'fecha': str})
        print(f"[EXTRACT] GA4: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        print(f"[EXTRACT] Error en GA4: {e}")
        return pd.DataFrame()


def extraer_google_ads():
    """Extrae datos de Google Ads."""
    try:
        path = os.path.join(DATA_RAW, 'google_ads_2025.csv')
        df = pd.read_csv(path)
        print(f"[EXTRACT] Google Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        print(f"[EXTRACT] Error en Google Ads: {e}")
        return pd.DataFrame()


def extraer_meta_ads():
    """Extrae datos de Meta Ads."""
    try:
        path = os.path.join(DATA_RAW, 'meta_ads_2025.csv')
        df = pd.read_csv(path)
        print(f"[EXTRACT] Meta Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        print(f"[EXTRACT] Error en Meta Ads: {e}")
        return pd.DataFrame()


def extraer_gsc():
    """Extrae datos de Google Search Console."""
    try:
        chart_path = os.path.join(DATA_RAW, 'gsc_chart_2025.csv')
        queries_path = os.path.join(DATA_RAW, 'gsc_queries_2025.csv')
        df_chart = pd.read_csv(chart_path)
        df_queries = pd.read_csv(queries_path)
        print(f"[EXTRACT] GSC Chart: {df_chart.shape[0]} filas | Queries: {df_queries.shape[0]} filas")
        return df_chart, df_queries
    except Exception as e:
        print(f"[EXTRACT] Error en GSC: {e}")
        return pd.DataFrame(), pd.DataFrame()


def extraer_ventas():
    """Extrae datos de ventas/polizas."""
    try:
        path = os.path.join(DATA_RAW, 'ventas_2025.csv')
        df = pd.read_csv(path)
        print(f"[EXTRACT] Ventas: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        print(f"[EXTRACT] Error en Ventas: {e}")
        return pd.DataFrame()


def extraer_todo():
    """Ejecuta toda la extraccion. Retorna tupla de DataFrames."""
    print("=" * 60)
    print("ETAPA: EXTRACCION")
    print("=" * 60)

    df_ga4 = extraer_ga4()
    df_gads = extraer_google_ads()
    df_meta = extraer_meta_ads()
    df_gsc_chart, df_gsc_queries = extraer_gsc()
    df_ventas = extraer_ventas()

    print(f"\n[EXTRACT] Extraccion completa: 5 fuentes cargadas")

    return df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas


if __name__ == '__main__':
    df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas = extraer_todo()
    print(f"\n  ga4: {df_ga4.shape}")
    print(f"  google_ads: {df_gads.shape}")
    print(f"  meta_ads: {df_meta.shape}")
    print(f"  gsc_chart: {df_gsc_chart.shape}")
    print(f"  gsc_queries: {df_gsc_queries.shape}")
    print(f"  ventas: {df_ventas.shape}")
