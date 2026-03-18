"""
transform.py — Modulo de Transformacion
Limpia, estandariza y une las fuentes en una Master Table.
"""
import pandas as pd


def limpiar_ga4(df):
    """Limpia datos de GA4: fechas, tipos, duplicados."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d', errors='coerce')
    for col in ['eventos', 'usuarios', 'sesiones', 'pageviews', 'nuevos_usuarios']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] GA4 limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


def limpiar_google_ads(df):
    """Limpia datos de Google Ads: fechas, tipos, calcula CPM."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    for col in ['impressions', 'clicks']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    for col in ['cost', 'conversions', 'ctr', 'avg_cpc']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    df['cpm'] = df.apply(
        lambda r: (r['cost'] / r['impressions'] * 1000) if r['impressions'] > 0 else 0, axis=1
    )
    df['fuente'] = 'google_ads'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Google Ads limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


def limpiar_meta_ads(df):
    """Limpia datos de Meta Ads: fechas, tipos."""
    df = df.copy()
    df['fecha_inicio'] = pd.to_datetime(df['date_start'], errors='coerce')
    df['fecha_fin'] = pd.to_datetime(df['date_stop'], errors='coerce')
    for col in ['impressions', 'clicks', 'reach']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    for col in ['spend', 'cpm', 'cpc', 'ctr', 'frequency']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    df['fuente'] = 'meta_ads'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Meta Ads limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


def limpiar_gsc(df_chart, df_queries):
    """Limpia datos de Google Search Console."""
    df_chart = df_chart.copy()
    df_chart['Date'] = pd.to_datetime(df_chart['Date'], errors='coerce')
    df_chart.rename(columns={
        'Date': 'fecha', 'Clicks': 'clicks',
        'Impressions': 'impressions', 'CTR': 'ctr', 'Position': 'position'
    }, inplace=True)
    if df_chart['ctr'].dtype == object:
        df_chart['ctr'] = df_chart['ctr'].str.rstrip('%').astype(float) / 100
    df_chart['fuente'] = 'gsc'

    df_queries = df_queries.copy()
    df_queries.rename(columns={
        'Top queries': 'query', 'Clicks': 'clicks',
        'Impressions': 'impressions', 'CTR': 'ctr', 'Position': 'position'
    }, inplace=True)
    if df_queries['ctr'].dtype == object:
        df_queries['ctr'] = df_queries['ctr'].str.rstrip('%').astype(float) / 100

    print(f"[TRANSFORM] GSC limpio: Chart {df_chart.shape[0]} filas | Queries {df_queries.shape[0]} filas")
    return df_chart, df_queries


def limpiar_ventas(df):
    """Limpia datos de ventas/polizas."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['FECINIVIG'], errors='coerce')
    df['monto'] = pd.to_numeric(df['MTOOPER'], errors='coerce').fillna(0.0)
    df['fuente'] = 'ventas'
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Ventas limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


def construir_master_table(df_ga4, df_gads, df_gsc_chart, df_ventas):
    """
    Construye la Master Table agregando por fecha y haciendo merge.
    Une: GA4 + Google Ads + GSC + Ventas, todo cruzado por fecha.
    """
    # Agrupar GA4 por fecha
    ga4_diario = df_ga4.groupby('fecha').agg(
        ga4_sesiones=('sesiones', 'sum'),
        ga4_usuarios=('usuarios', 'sum'),
        ga4_pageviews=('pageviews', 'sum'),
        ga4_nuevos=('nuevos_usuarios', 'sum')
    ).reset_index()

    # Agrupar Google Ads por fecha
    gads_diario = df_gads.groupby('fecha').agg(
        gads_impressions=('impressions', 'sum'),
        gads_clicks=('clicks', 'sum'),
        gads_cost=('cost', 'sum'),
        gads_conversions=('conversions', 'sum')
    ).reset_index()
    gads_diario['gads_cpm'] = gads_diario.apply(
        lambda r: (r['gads_cost'] / r['gads_impressions'] * 1000) if r['gads_impressions'] > 0 else 0, axis=1
    )
    gads_diario['gads_cpc'] = gads_diario.apply(
        lambda r: (r['gads_cost'] / r['gads_clicks']) if r['gads_clicks'] > 0 else 0, axis=1
    )

    # GSC por fecha
    gsc_diario = df_gsc_chart[['fecha', 'clicks', 'impressions']].copy()
    gsc_diario.rename(columns={'clicks': 'gsc_clicks', 'impressions': 'gsc_impressions'}, inplace=True)

    # Ventas por fecha
    ventas_diario = df_ventas.groupby('fecha').agg(
        ventas_cantidad=('NUMPOL', 'count'),
        ventas_monto=('monto', 'sum')
    ).reset_index()

    # Merge todo por fecha (left join secuencial)
    master = ga4_diario.merge(gads_diario, on='fecha', how='outer')
    master = master.merge(gsc_diario, on='fecha', how='outer')
    master = master.merge(ventas_diario, on='fecha', how='outer')
    master = master.sort_values('fecha').reset_index(drop=True)
    master = master.fillna(0)

    print(f"\n[TRANSFORM] Master Table: {master.shape[0]} filas, {master.shape[1]} columnas")
    return master


def transformar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas):
    """Ejecuta toda la transformacion. Recibe tupla, retorna tupla."""
    print("\n" + "=" * 60)
    print("ETAPA: TRANSFORMACION")
    print("=" * 60)

    try:
        df_ga4 = limpiar_ga4(df_ga4)
        df_gads = limpiar_google_ads(df_gads)
        df_meta = limpiar_meta_ads(df_meta)
        df_gsc_chart, df_gsc_queries = limpiar_gsc(df_gsc_chart, df_gsc_queries)
        df_ventas = limpiar_ventas(df_ventas)
        master = construir_master_table(df_ga4, df_gads, df_gsc_chart, df_ventas)
    except Exception as e:
        print(f"[TRANSFORM] Error: {e}")
        master = pd.DataFrame()

    return df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master
