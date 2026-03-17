"""
load.py — Modulo de Carga
Proyecto Final ETL — Maestria en IA y Ciencia de Datos (UAO)

Exporta la Master Table y genera reporte de calidad.
"""
import pandas as pd
import os

DATA_PROCESSED = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')


def load_master_table(master_table):
    """Guarda la Master Table como CSV en data/processed/."""
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    outpath = os.path.join(DATA_PROCESSED, 'master_table.csv')
    master_table.to_csv(outpath, index=False)
    print(f"\n[LOAD] Master Table guardada en: {outpath}")
    print(f"[LOAD] Filas: {master_table.shape[0]} | Columnas: {master_table.shape[1]}")
    return outpath


def generate_quality_report(transformed_data):
    """Genera un reporte de calidad de los datos transformados."""
    print("\n" + "=" * 60)
    print("REPORTE DE CALIDAD")
    print("=" * 60)
    for name, df in transformed_data.items():
        nulls = df.isnull().sum().sum()
        dupes = df.duplicated().sum()
        print(f"  {name:15s} | Filas: {df.shape[0]:>6} | Cols: {df.shape[1]:>3} | Nulls: {nulls:>5} | Dupes: {dupes:>4}")


def load_all(transformed_data):
    """Ejecuta toda la carga."""
    print("\n" + "=" * 60)
    print("ETAPA: CARGA")
    print("=" * 60)
    outpath = load_master_table(transformed_data['master_table'])
    generate_quality_report(transformed_data)
    print(f"\n[LOAD] Proceso de carga completado exitosamente")
    return outpath
