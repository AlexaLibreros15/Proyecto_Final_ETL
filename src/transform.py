"""
transform.py — Modulo de Transformacion
Proyecto Final ETL — Maestria en IA y Ciencia de Datos (UAO)

Limpia, estandariza y une las fuentes de datos en una Master Table.
"""
import pandas as pd


def clean_ga4(df):
    """Limpia y estandariza datos de GA4."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d')
    # Convertir metricas a numerico
    for col in ['eventos', 'usuarios', 'sesiones', 'pageviews', 'nuevos_usuarios']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] GA4 limpio: {df.shape[0]} filas")
    return df


def clean_google_ads(df):
    """Limpia y estandariza datos de Google Ads."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    for col in ['impressions', 'clicks']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    for col in ['cost', 'conversions', 'ctr', 'avg_cpc']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    # Calcular CPM
    df['cpm'] = df.apply(
        lambda r: (r['cost'] / r['impressions'] * 1000) if r['impressions'] > 0 else 0, axis=1
    )
    df['fuente'] = 'google_ads'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Google Ads limpio: {df.shape[0]} filas")
    return df


def clean_meta_ads(df):
    """Limpia y estandariza datos de Meta Ads."""
    df = df.copy()
    df['fecha_inicio'] = pd.to_datetime(df['date_start'])
    df['fecha_fin'] = pd.to_datetime(df['date_stop'])
    for col in ['impressions', 'clicks', 'reach']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    for col in ['spend', 'cpm', 'cpc', 'ctr', 'frequency']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    df['fuente'] = 'meta_ads'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Meta Ads limpio: {df.shape[0]} filas")
    return df


def clean_gsc(df_chart, df_queries):
    """Limpia datos de Google Search Console."""
    df_chart = df_chart.copy()
    df_chart['Date'] = pd.to_datetime(df_chart['Date'])
    df_chart.rename(columns={'Date': 'fecha', 'Clicks': 'clicks', 'Impressions': 'impressions',
                              'CTR': 'ctr', 'Position': 'position'}, inplace=True)
    # CTR viene como "4.17%" -> convertir a decimal
    if df_chart['ctr'].dtype == object:
        df_chart['ctr'] = df_chart['ctr'].str.rstrip('%').astype(float) / 100
    df_chart['fuente'] = 'gsc'

    df_queries = df_queries.copy()
    df_queries.rename(columns={'Top queries': 'query', 'Clicks': 'clicks',
                                'Impressions': 'impressions', 'CTR': 'ctr',
                                'Position': 'position'}, inplace=True)
    if df_queries['ctr'].dtype == object:
        df_queries['ctr'] = df_queries['ctr'].str.rstrip('%').astype(float) / 100

    print(f"[TRANSFORM] GSC Chart limpio: {df_chart.shape[0]} filas | Queries: {df_queries.shape[0]} filas")
    return df_chart, df_queries


def clean_ventas(df):
    """Limpia datos de ventas/polizas."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['FECINIVIG'])
    df['monto'] = pd.to_numeric(df['MTOOPER'], errors='coerce').fillna(0.0)
    df['fuente'] = 'ventas'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Ventas limpio: {df.shape[0]} filas")
    return df


def build_master_table(ga4, gads, meta, gsc_chart, ventas):
    """
    Construye la Master Table agregando datos por fecha.
    Une pauta (Google Ads + Meta), trafico (GA4), SEO (GSC) y ventas por fecha.
    """
    # Agregar GA4 por fecha
    ga4_daily = ga4.groupby('fecha').agg(
        ga4_sesiones=('sesiones', 'sum'),
        ga4_usuarios=('usuarios', 'sum'),
        ga4_pageviews=('pageviews', 'sum'),
        ga4_nuevos=('nuevos_usuarios', 'sum')
    ).reset_index()

    # Agregar Google Ads por fecha
    gads_daily = gads.groupby('fecha').agg(
        gads_impressions=('impressions', 'sum'),
        gads_clicks=('clicks', 'sum'),
        gads_cost=('cost', 'sum'),
        gads_conversions=('conversions', 'sum')
    ).reset_index()
    gads_daily['gads_cpm'] = gads_daily.apply(
        lambda r: (r['gads_cost'] / r['gads_impressions'] * 1000) if r['gads_impressions'] > 0 else 0, axis=1
    )
    gads_daily['gads_cpc'] = gads_daily.apply(
        lambda r: (r['gads_cost'] / r['gads_clicks']) if r['gads_clicks'] > 0 else 0, axis=1
    )

    # GSC por fecha
    gsc_daily = gsc_chart[['fecha', 'clicks', 'impressions']].copy()
    gsc_daily.rename(columns={'clicks': 'gsc_clicks', 'impressions': 'gsc_impressions'}, inplace=True)

    # Ventas por fecha
    ventas_daily = ventas.groupby('fecha').agg(
        ventas_cantidad=('NUMPOL', 'count'),
        ventas_monto=('monto', 'sum')
    ).reset_index()

    # Merge todo por fecha
    master = ga4_daily.merge(gads_daily, on='fecha', how='outer')
    master = master.merge(gsc_daily, on='fecha', how='outer')
    master = master.merge(ventas_daily, on='fecha', how='outer')
    master = master.sort_values('fecha').reset_index(drop=True)
    master = master.fillna(0)

    print(f"\n[TRANSFORM] Master Table: {master.shape[0]} filas, {master.shape[1]} columnas")
    return master


def transform_all(data):
    """Ejecuta toda la transformacion."""
    print("\n" + "=" * 60)
    print("ETAPA: TRANSFORMACION")
    print("=" * 60)
    ga4 = clean_ga4(data['ga4'])
    gads = clean_google_ads(data['google_ads'])
    meta = clean_meta_ads(data['meta_ads'])
    gsc_chart, gsc_queries = clean_gsc(data['gsc_chart'], data['gsc_queries'])
    ventas = clean_ventas(data['ventas'])

    master = build_master_table(ga4, gads, meta, gsc_chart, ventas)

    return {
        'ga4': ga4,
        'google_ads': gads,
        'meta_ads': meta,
        'gsc_chart': gsc_chart,
        'gsc_queries': gsc_queries,
        'ventas': ventas,
        'master_table': master
    }
