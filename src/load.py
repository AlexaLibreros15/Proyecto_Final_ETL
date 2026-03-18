"""
load.py — Modulo de Carga
Exporta la Master Table a CSV y genera reporte de calidad.
"""
import pandas as pd
import os

DATA_PROCESSED = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')


def cargar_master_table(master_table):
    """Guarda la Master Table como CSV en data/processed/."""
    try:
        os.makedirs(DATA_PROCESSED, exist_ok=True)
        outpath = os.path.join(DATA_PROCESSED, 'master_table.csv')
        master_table.to_csv(outpath, index=False)
        print(f"\n[LOAD] Master Table guardada en: {outpath}")
        print(f"[LOAD] Filas: {master_table.shape[0]} | Columnas: {master_table.shape[1]}")
        return outpath
    except Exception as e:
        print(f"[LOAD] Error al guardar: {e}")
        return None


def reporte_calidad(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master):
    """Imprime reporte de calidad de todos los DataFrames."""
    print("\n" + "=" * 60)
    print("REPORTE DE CALIDAD")
    print("=" * 60)
    datos = {
        'ga4': df_ga4, 'google_ads': df_gads, 'meta_ads': df_meta,
        'gsc_chart': df_gsc_chart, 'gsc_queries': df_gsc_queries,
        'ventas': df_ventas, 'master_table': master
    }
    for nombre, df in datos.items():
        nulls = df.isnull().sum().sum()
        dupes = df.duplicated().sum()
        print(f"  {nombre:15s} | Filas: {df.shape[0]:>6} | Cols: {df.shape[1]:>3} | Nulls: {nulls:>5} | Dupes: {dupes:>4}")


def cargar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master):
    """Ejecuta toda la carga. Recibe tupla de DataFrames."""
    print("\n" + "=" * 60)
    print("ETAPA: CARGA")
    print("=" * 60)
    outpath = cargar_master_table(master)
    reporte_calidad(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master)
    print(f"\n[LOAD] Proceso de carga completado")
    return outpath
