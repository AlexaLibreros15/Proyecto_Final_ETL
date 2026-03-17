"""
pipeline.py — Orquestador del Pipeline ETL
Proyecto Final ETL — Maestria en IA y Ciencia de Datos (UAO)

Ejecuta el flujo completo: Extraccion -> Transformacion -> Carga
Uso: python src/pipeline.py
"""
import time
from extract import extract_all
from transform import transform_all
from load import load_all


def run_pipeline():
    """Ejecuta el pipeline ETL completo."""
    print("*" * 60)
    print("  PIPELINE ETL — Publicidad Digital Cliente_A (2025)")
    print("*" * 60)
    start = time.time()

    # E — Extraccion
    raw_data = extract_all()

    # T — Transformacion
    transformed_data = transform_all(raw_data)

    # L — Carga
    output_path = load_all(transformed_data)

    elapsed = time.time() - start
    print("\n" + "*" * 60)
    print(f"  PIPELINE COMPLETADO en {elapsed:.1f} segundos")
    print(f"  Archivo generado: {output_path}")
    print("*" * 60)

    return transformed_data


if __name__ == '__main__':
    run_pipeline()
