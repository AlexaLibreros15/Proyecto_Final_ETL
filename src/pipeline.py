"""
pipeline.py — Orquestador del Pipeline ETL
Ejecuta el flujo completo: Extraccion -> Transformacion -> Carga
Uso: python pipeline.py
"""
import time
from extract import extraer_todo
from transform import transformar_todo
from load import cargar_todo


def main():
    """Ejecuta el pipeline ETL completo."""
    print("*" * 60)
    print("  PIPELINE ETL — Publicidad Digital Cliente_A (2025)")
    print("*" * 60)
    start = time.time()

    # E — Extraccion: retorna tupla de 6 DataFrames
    df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas = extraer_todo()

    # T — Transformacion: recibe 6, retorna 7 (los 6 limpios + master)
    df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master = transformar_todo(
        df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas
    )

    # L — Carga: recibe los 7 DataFrames, guarda master y genera reporte
    outpath = cargar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master)

    elapsed = time.time() - start
    print("\n" + "*" * 60)
    print(f"  PIPELINE COMPLETADO en {elapsed:.1f} segundos")
    print(f"  Archivo generado: {outpath}")
    print("*" * 60)


if __name__ == '__main__':
    main()
