import streamlit as st
import pandas as pd
import duckdb
import folium
from streamlit_folium import st_folium
import os

# Configuración de la página web
st.set_page_config(
    page_title="Monitoreo Climático - Posadas",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Sistema de Alertas Meteorológicas - Posadas, Misiones")
st.markdown("Dashboard profesional de ingeniería de datos alimentado por una arquitectura Medallón (DuckDB + Parquet).")

# --- CARGA DE DATOS (Capa Gold) ---
@st.cache_data
def cargar_datos_gold():
    con = duckdb.connect()
    # Usamos rutas relativas desde la raíz del proyecto
    df_alerts = con.execute("SELECT * FROM read_parquet('Data/gold/weather_alerts.parquet')").df()
    df_daily = con.execute("SELECT * FROM read_parquet('Data/gold/weather_daily_summary.parquet')").df()
    return df_alerts, df_daily

try:
    df_alerts, df_daily = cargar_datos_gold()
    
    # --- SECCIÓN 1: ALERTAS ACTIVAS ---
    st.subheader("🚨 Alertas Críticas Detectadas (Próximos 7 días)")
    
    alertas_reales = df_alerts[df_alerts['tiene_alerta'] == 1]
    
    if not alertas_reales.empty:
        st.warning(f"⚠️ Se han detectado {len(alertas_reales)} horas con condiciones extremas pronosticadas.")
        for tipo_alerta in alertas_reales['estado_alerta'].unique():
            st.error(f"**{tipo_alerta}**")
            
        with st.expander("Ver detalle de horas críticas"):
            st.dataframe(alertas_reales[['fecha_hora', 'temperatura_celsius', 'lluvia_mm', 'estado_alerta']].rename(
                columns={'fecha_hora': 'Fecha/Hora', 'temperatura_celsius': 'Temp (°C)', 'lluvia_mm': 'Lluvia (mm)', 'estado_alerta': 'Alerta'}
            ), use_container_width=True)
    else:
        st.success("🟢 No se detectaron alertas de temperaturas extremas ni tormentas fuertes para los próximos días.")

    st.markdown("---")

    # --- SECCIÓN 2: KPIs Y MAPA ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📍 Ubicación del Monitoreo")
        mapa = folium.Map(location=[-27.3671, -55.8961], zoom_start=12)
        folium.Marker(
            [-27.3671, -55.8961], 
            popup="Posadas, Misiones", 
            tooltip="Punto de Ingesta del Pipeline",
            icon=folium.Icon(color="red", icon="cloud")
        ).add_to(mapa)
        
        st_folium(mapa, height=300, width=None)

    with col2:
        st.subheader("📅 Pronóstico y Resumen Diario")
        st.dataframe(df_daily.rename(
            columns={
                'fecha': 'Fecha',
                'temp_maxima': 'Máxima (°C)',
                'temp_minima': 'Mínima (°C)',
                'humedad_promedio': 'Humedad Prom. (%)',
                'lluvia_total_mm': 'Lluvia Total (mm)',
                'alerta_del_dia': 'Estado del Día'
            }
        ), use_container_width=True, hide_index=True)

    # --- SECCIÓN 3: GRÁFICO ---
    st.markdown("---")
    st.subheader("📈 Evolución de la Temperatura")
    df_alerts_chart = df_alerts.set_index('fecha_hora')
    st.line_chart(df_alerts_chart['temperatura_celsius'], y_label="Temperatura (°C)", x_label="Fecha y Hora")

except Exception as e:
    st.error("Error al cargar los archivos de la capa Gold. Asegúrate de haber ejecutado todos los notebooks anteriores.")
    st.info(f"Detalle del error: {e}")