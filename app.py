"""
app.py — Dashboard Streamlit
Análisis Publicitario 2025 — Cliente A
Carga la master_table generada por pipeline.py y los CSVs raw para métricas de canal.
"""
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

BASE = os.path.dirname(os.path.abspath(__file__))
COLORS = {
    'azul':   '#1B4F72',
    'azul_l': '#AED6F1',
    'verde':  '#27AE60',
    'naranja':'#E67E22',
    'rojo':   '#E74C3C',
    'gris':   '#BDC3C7',
}
MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']


# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Publicitario 2025 — Cliente A",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    master   = pd.read_csv(os.path.join(BASE, 'data/processed/master_table.csv'),
                           parse_dates=['fecha'])
    master['ventas_usd'] = master['ventas_monto'] / 7.7   # QTZ → USD

    gads_raw  = pd.read_csv(os.path.join(BASE, 'data/raw/google_ads_2025.csv'),
                            parse_dates=['fecha'])
    meta_raw  = pd.read_csv(os.path.join(BASE, 'data/raw/meta_ads_2025.csv'),
                            parse_dates=['date_start'])
    meta_raw['spend'] = meta_raw['spend'].astype(float)
    ventas_raw = pd.read_csv(os.path.join(BASE, 'data/raw/ventas_2025.csv'),
                             parse_dates=['FECINIVIG'])
    ventas_raw['monto_usd'] = ventas_raw['MTOOPER'].astype(float) / 7.7
    return master, gads_raw, meta_raw, ventas_raw

df, df_gads, df_meta, df_ventas = load_data()

# ── KPIs agregados ───────────────────────────────────────────────────────────
total_inv    = round(df_gads['cost'].sum() + df_meta['spend'].sum())
total_pol    = len(df_ventas)
total_rev    = round(df_ventas['monto_usd'].sum())
roas         = round(total_rev / total_inv, 2)
cpa          = round(total_inv / total_pol)
aov          = round(total_rev / total_pol)

# ── Series mensuales ─────────────────────────────────────────────────────────
df['mes'] = df['fecha'].dt.month
df_gads['mes'] = df_gads['fecha'].dt.month
df_meta['mes'] = df_meta['date_start'].dt.month
df_ventas['mes'] = df_ventas['FECINIVIG'].dt.month

inv_gads_mes = df_gads.groupby('mes')['cost'].sum()
inv_meta_mes = df_meta.groupby('mes')['spend'].sum()
inv_mes      = [(inv_gads_mes.get(m, 0) + inv_meta_mes.get(m, 0)) for m in range(1,13)]
pol_mes      = [int(df_ventas[df_ventas['mes']==m].shape[0]) for m in range(1,13)]
rev_mes      = [round(df_ventas[df_ventas['mes']==m]['monto_usd'].sum()) for m in range(1,13)]
ga4_mes      = [int(df[df['mes']==m]['ga4_sesiones'].sum()) for m in range(1,13)]
gsc_clics    = [int(df[df['mes']==m]['gsc_clicks'].sum()) for m in range(1,13)]
gsc_impr     = [int(df[df['mes']==m]['gsc_impressions'].sum()) for m in range(1,13)]


# ════════════════════════════════════════════════════════════════════════════
# ENCABEZADO
# ════════════════════════════════════════════════════════════════════════════
st.markdown(
    f"<h2 style='color:#1B4F72;line-height:1.4'>En 2025, Cliente A invirtió "
    f"<strong>${total_inv:,}</strong> en publicidad digital y vendió "
    f"<strong>{total_pol:,} pólizas</strong> — un retorno de "
    f"<strong>${roas}x</strong> por cada $1 invertido</h2>",
    unsafe_allow_html=True
)
st.caption(
    "Google Ads · Meta Ads · Google Analytics · Search Console · Ventas | "
    "Pipeline ETL automático en Python · Ventas en QTZ convertidas a USD (÷7.7) · "
    "Repositorio: github.com/AlexaLibreros15/Proyecto_Final_ETL"
)
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# KPIs
# ════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Inversión total",           f"${total_inv:,}",  "Todo 2025, en USD")
c2.metric("Ventas generadas",          f"${total_rev:,}",  f"{total_pol:,} pólizas")
c3.metric("Retorno sobre inversión",   f"{roas}x",         f"${roas} por cada $1")
c4.metric("Costo por póliza",          f"${cpa}",          "Inversión ÷ pólizas")
c5.metric("Valor promedio de póliza",  f"${aov}",          "Ticket promedio USD")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — Inversión por canal
# ════════════════════════════════════════════════════════════════════════════
st.subheader("1 · Google Ads concentró el 81% del presupuesto — y dentro de Google, Performance Max fue el formato más eficiente")
st.caption("El presupuesto se repartió entre Google Ads ($42,658) y Meta Ads ($10,248). Dentro de Google, los 4 tipos de campaña tuvieron rendimientos muy distintos.")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5, 4))
    vals = [df_gads['cost'].sum(), df_meta['spend'].sum()]
    labels = [f"Google Ads\n${vals[0]:,.0f} (81%)", f"Meta Ads\n${vals[1]:,.0f} (19%)"]
    ax.pie(vals, labels=labels, colors=[COLORS['azul'], COLORS['naranja']],
           startangle=90, wedgeprops={'linewidth':0})
    ax.set_title("Distribución del presupuesto por canal", fontsize=11, pad=12)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* Meta Ads representa el 19% del presupuesto pero no tiene trazabilidad directa hacia pólizas vendidas — su contribución a ventas no puede confirmarse con los datos actuales.")

with col2:
    fig, ax1 = plt.subplots(figsize=(5, 4))
    tipos     = ['Search', 'Perf. Max', 'Demand Gen', 'Display']
    inv_t     = [31811, 6575, 2282, 1989]
    cpa_t     = [7.61, 1.36, 19.47, 34.63]
    colores   = [COLORS['azul']+'cc', COLORS['verde']+'cc', COLORS['azul_l'], COLORS['gris']]
    x = range(len(tipos))
    bars = ax1.bar(x, inv_t, color=colores, width=0.5)
    ax1.set_ylabel("Inversión USD", fontsize=9)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax1.set_xticks(x); ax1.set_xticklabels(tipos, fontsize=9)
    ax2 = ax1.twinx()
    ax2.plot(x, cpa_t, color=COLORS['rojo'], marker='o', linewidth=2, markersize=7)
    ax2.set_ylabel("Costo por conversión USD", fontsize=9, color=COLORS['rojo'])
    ax2.tick_params(axis='y', colors=COLORS['rojo'])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:.0f}"))
    ax1.set_title("Inversión vs costo por conversión por tipo de campaña", fontsize=11)
    ax1.grid(axis='y', color='#eee', linewidth=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* Performance Max logró el menor costo por conversión con solo el 15% del presupuesto de Google; Display gastó una proporción similar y costó 25 veces más por cada conversión obtenida.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Comportamiento mensual
# ════════════════════════════════════════════════════════════════════════════
st.subheader("2 · La inversión fluctuó entre $2,143 y $6,413 — sin una relación directa entre meses de alta inversión y meses de más ventas")
st.caption("Ver cómo varió el presupuesto mes a mes permite identificar si la empresa apostó más en los momentos correctos.")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(MESES, inv_mes, color=COLORS['azul']+'cc', width=0.6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.set_title("Inversión mensual (Google Ads + Meta Ads)", fontsize=11)
    ax.grid(axis='y', color='#eee', linewidth=0.5); ax.set_axisbelow(True)
    plt.xticks(fontsize=8); plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* Septiembre y octubre tuvieron la menor inversión del año y al mismo tiempo el mayor tráfico web — el tráfico orgánico compensó la reducción de pauta en esos meses.")

with col2:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(MESES, pol_mes, color=COLORS['verde']+'99', width=0.6)
    ax.set_title("Pólizas vendidas por mes", fontsize=11)
    ax.grid(axis='y', color='#eee', linewidth=0.5); ax.set_axisbelow(True)
    plt.xticks(fontsize=8); plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* La diferencia entre el mes más bajo (noviembre, 69) y el más alto (marzo, 107) es del 55% — una distribución estable que no sigue los picos de inversión publicitaria.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Ventas y productos
# ════════════════════════════════════════════════════════════════════════════
st.subheader("3 · El 96% de las pólizas son Auto por Kilómetro, pero Auto Tradicional vale 3.3 veces más por póliza")
st.caption("Cliente A vende dos tipos de seguro: Auto por Kilómetro y Auto Tradicional. Los montos en Quetzales guatemaltecos se convirtieron a USD (÷7.7).")

col1, col2 = st.columns(2)

prod_col = next(c for c in df_ventas.columns if 'PROD' in c.upper() or 'TIP' in c.upper())
prod_counts = df_ventas.groupby(prod_col).agg(
    cantidad=('monto_usd', 'count'),
    revenue=('monto_usd', 'sum')
).reset_index()

with col1:
    fig, ax = plt.subplots(figsize=(5, 4))
    labels_p = [f"{r[prod_col]}\n{r['cantidad']} pólizas · ${r['revenue']/r['cantidad']:,.0f} prom" for _, r in prod_counts.iterrows()]
    ax.pie(prod_counts['cantidad'], labels=labels_p,
           colors=[COLORS['azul'], COLORS['naranja']], startangle=90, wedgeprops={'linewidth':0})
    ax.set_title("Pólizas vendidas por producto", fontsize=11, pad=12)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* Auto Tradicional representa solo el 4% de las pólizas vendidas pero genera el 13% del revenue — una sola póliza Tradicional equivale en valor a 3.3 pólizas KM.")

with col2:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    x = range(12)
    w = 0.4
    ax.bar([i - w/2 for i in x], rev_mes, width=w, label='Ventas USD', color=COLORS['verde']+'99')
    ax.bar([i + w/2 for i in x], inv_mes, width=w, label='Inversión USD', color=COLORS['azul']+'99')
    ax.set_xticks(x); ax.set_xticklabels(MESES, fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.set_title("Ventas vs inversión mensual", fontsize=11)
    ax.legend(fontsize=9); ax.grid(axis='y', color='#eee', linewidth=0.5); ax.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* Marzo registró el mayor revenue del año con una de las menores inversiones del primer semestre — la brecha más amplia entre ventas e inversión de todo el año.")

col1, col2, col3 = st.columns(3)
col1.metric("Revenue Auto KM",         f"${round(prod_counts[prod_counts[prod_col].str.contains('KM', na=False)]['revenue'].sum()):,}", "87% del total")
col2.metric("Revenue Auto Tradicional", f"${round(prod_counts[~prod_counts[prod_col].str.contains('KM', na=False)]['revenue'].sum()):,}", "13% del total")
col3.metric("Costo promedio por póliza", f"${cpa}", "Inversión ÷ pólizas")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Tráfico web
# ════════════════════════════════════════════════════════════════════════════
total_ga4 = sum(ga4_mes)
st.subheader(f"4 · El sitio recibió {total_ga4:,} visitas en 2025 — el tráfico del segundo semestre triplicó al del primero")
st.caption("Google Analytics 4 registra cada visita al sitio. Datos desde el 23 de enero (día de activación del sistema).")

fig, ax = plt.subplots(figsize=(10, 3.5))
bar_colors = [COLORS['gris']] + [COLORS['azul'] if v > 40000 else COLORS['azul_l'] if v > 20000 else COLORS['gris']+'99' for v in ga4_mes[1:]]
ax.bar(MESES, ga4_mes, color=bar_colors, width=0.6)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}K"))
ax.set_title("Sesiones web mensuales (Google Analytics 4)", fontsize=11)
ax.grid(axis='y', color='#eee', linewidth=0.5); ax.set_axisbelow(True)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
st.caption("*Nota.* El segundo semestre (jul–dic) concentró el 72% de todas las visitas del año con menor inversión publicitaria — señal de que el canal orgánico ganó peso progresivamente a lo largo del año.")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — Búsquedas orgánicas
# ════════════════════════════════════════════════════════════════════════════
total_clics = sum(gsc_clics)
total_impr  = sum(gsc_impr)
ctr_anual   = round(total_clics / total_impr * 100, 1)
st.subheader(f"5 · El sitio apareció {total_impr:,} veces en Google y recibió {total_clics:,} clics orgánicos — CTR de {ctr_anual}%")
st.caption("Search Console mide cuándo el sitio aparece en resultados de Google sin pagar. Complementa la inversión pagada.")

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax1 = plt.subplots(figsize=(6, 3.5))
    x = range(12)
    ax1.bar(x, gsc_impr, color=COLORS['azul_l']+'cc', width=0.6, label='Impresiones')
    ax1.set_ylabel("Impresiones", fontsize=9)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}K" if v >= 1000 else str(int(v))))
    ax2 = ax1.twinx()
    ax2.plot(x, gsc_clics, color=COLORS['azul'], marker='o', linewidth=2, markersize=6, label='Clics')
    ax2.set_ylabel("Clics orgánicos", fontsize=9, color=COLORS['azul'])
    ax2.tick_params(axis='y', colors=COLORS['azul'])
    ax1.set_xticks(x); ax1.set_xticklabels(MESES, fontsize=8)
    ax1.set_title("Visibilidad orgánica mensual (Search Console)", fontsize=11)
    ax1.grid(axis='y', color='#eee', linewidth=0.5); ax1.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("*Nota.* La posición promedio 4.2 indica primer resultado en Google — pero solo 1 de cada 22 personas que ven el resultado hace clic, señalando una oportunidad en el título y descripción de la página.")

with col2:
    st.metric("Apariciones en Google",  f"{total_impr:,}")
    st.metric("Clics orgánicos",        f"{total_clics:,}")
    st.metric("Tasa de clic (CTR)",     f"{ctr_anual}%",    "c/100 apariciones")
    st.metric("Posición promedio",      "4.2",              "1er resultado Google")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — Qué funcionó / qué no
# ════════════════════════════════════════════════════════════════════════════
st.subheader("6 · Performance Max fue la pieza más eficiente del portafolio — las campañas de conversión en Meta no tuvieron trazabilidad hacia ventas reales")
st.caption("Lectura descriptiva consolidando las 5 fuentes. Identifica qué mantener, qué reformular y dónde existe oportunidad para 2026.")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("**✓ Funcionó — mantener**")
    st.success(
        "**Performance Max:** 15% del presupuesto Google, $1.36/conversión — el más bajo de todos los formatos.\n\n"
        "**Search:** 75% del presupuesto, 4,179 conversiones a $7.61 c/u. Canal predecible.\n\n"
        "**Meta Tráfico:** 186,688 visitas a $0.02 por clic.\n\n"
        "**Auto KM:** 967 pólizas vendidas los 12 meses sin excepción."
    )

with c2:
    st.markdown("**✗ No funcionó — revisar**")
    st.error(
        "**Meta Conversiones (WhatsApp):** $4,262 → 22 mensajes a $193 c/u. Sin trazabilidad a pólizas.\n\n"
        "**Display:** $1,989 con 57 conversiones a $34.63 c/u — 25x más caro que Performance Max.\n\n"
        "**Abril:** $6,286 invertidos generaron el peor costo por póliza del año ($84)."
    )

with c3:
    st.markdown("**? Sin dato suficiente**")
    st.warning(
        "**¿WhatsApp → pólizas?** Los 22 mensajes de Meta no tienen número de póliza asociado. Se necesita conectar CRM con Meta.\n\n"
        "**¿Meta Sep-Nov generó ventas?** Hay correlación temporal pero no causalidad. Sin UTMs en formularios no se puede confirmar."
    )

with c4:
    st.markdown("**→ Oportunidad 2026**")
    st.info(
        "**Auto Tradicional:** 44 pólizas a $560 promedio. Una campaña específica podría aumentar revenue sin más presupuesto.\n\n"
        "**Reasignar Display a PMax:** Los $1,989 de Display rinden 25x más en Performance Max.\n\n"
        "**Conectar WhatsApp + CRM:** Si se rastrea la conversión, Meta podría mostrar mucho más valor."
    )

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7 — El pipeline ETL
# ════════════════════════════════════════════════════════════════════════════
st.subheader("7 · 5 fuentes con formatos distintos se unifican en 0.4 segundos — antes esto requería trabajo manual en 5 hojas de cálculo separadas")
st.caption("El pipeline ETL (Extracción, Transformación y Carga) lee, limpia y une los datos automáticamente. 4 archivos modulares: extract.py, transform.py, load.py, pipeline.py.")

pipeline_data = {
    "Fuente":             ["Google Ads", "Meta Ads", "Google Analytics 4", "Search Console", "Ventas / Pólizas"],
    "Registros":          ["1,219 filas", "26 filas", "7,446 filas", "335 filas", "1,011 filas"],
    "Columnas":           [9, 14, 9, 5, 6],
    "Método extracción":  ["API REST v23", "Graph API v22.0", "BigQuery SQL", "CSV manual", "CSV manual"],
    "Qué aporta":         [
        "Inversión, clics, conversiones diarias por campaña",
        "Inversión, alcance, frecuencia mensual por campaña",
        "Visitas, fuente de tráfico, páginas vistas por día",
        "Apariciones en Google, clics orgánicos, posición",
        "Póliza, producto, fecha, monto en Quetzales"
    ]
}
st.dataframe(pd.DataFrame(pipeline_data), use_container_width=True, hide_index=True)
st.info(f"**Resultado:** 9,417+ registros de 5 fuentes → Master Table de 363 filas × 16 columnas (una fila por día). "
        f"Conversión QTZ → USD aplicada en transform.py (÷7.7).")

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Pipeline ETL · Python + pandas + matplotlib · Streamlit · "
    "Repositorio: github.com/AlexaLibreros15/Proyecto_Final_ETL · "
    "Dashboard HTML: thepipo93.github.io/etl-dashboard-ipalmera · "
    "Equipo: Christian Trujillo · Juan Sebastián Hoyos · Koraima Torres · Alexandra Libreros · "
    "UAO Maestría IA y Ciencia de Datos 2026-1S"
)
