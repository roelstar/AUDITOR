import streamlit as st
import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
from datetime import date
from io import BytesIO

st.set_page_config(
    page_title="ROELSTAR | Diagnóstico Financiero Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta ROELSTAR
DARK = "#20242B"
RED = "#D62828"
LIGHT = "#F4F6F8"
GREEN = "#18864B"
AMBER = "#D97706"

st.markdown(f"""
<style>
    .stApp {{ background: {LIGHT}; }}
    [data-testid="stSidebar"] {{ background: {DARK}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    .roelstar-header {{
        background: linear-gradient(120deg, {DARK} 0%, #353B45 100%);
        border-left: 8px solid {RED}; border-radius: 14px;
        padding: 24px 28px; color: white; margin-bottom: 18px;
    }}
    .roelstar-header h1 {{ color: white; margin: 0; font-size: 2rem; }}
    .roelstar-header p {{ color: #E7E9EC; margin: 6px 0 0 0; }}
    div[data-testid="stMetric"] {{
        background: white; border: 1px solid #E3E6EA;
        padding: 14px 16px; border-radius: 12px;
    }}
    .section-label {{ color: {RED}; font-weight: 750; letter-spacing: .04em; }}
    .small-note {{ color: #606975; font-size: .88rem; }}
    .status-good {{ color: {GREEN}; font-weight: 700; }}
    .status-warn {{ color: {AMBER}; font-weight: 700; }}
    .status-bad {{ color: {RED}; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

def money(value):
    try:
        return "$" + f"{float(value):,.0f}".replace(",", ".")
    except Exception:
        return "$0"

def pct(value):
    return f"{value:.1f}%"

# Encabezado original ROELSTAR: se conserva el diseño y solo se sustituye la estrella por el logo oficial.
logo_path = Path(__file__).with_name("roelstar_logo.png")
logo_html = ""
if logo_path.exists():
    logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    logo_html = (
        '<div style="background:#FFFFFF;border-radius:10px;padding:8px 12px;'
        'display:inline-flex;align-items:center;justify-content:center;">'
        f'<img src="data:image/png;base64,{logo_b64}" '
        'style="width:260px;max-width:100%;height:auto;display:block;" alt="ROELSTAR">'
        '</div>'
    )
else:
    logo_html = '<h1 style="color:white;margin:0;">★ ROELSTAR</h1>'

st.markdown(f"""
<div class="roelstar-header">
  {logo_html}
  <p style="margin-top:14px;">DIAGNÓSTICO FINANCIERO EMPRESARIAL · SERVICIOS Y TALLER TÉCNICO</p>
  <p>Control mensual de rentabilidad, costos, punto de equilibrio y caja</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Parámetros del análisis")
    empresa = st.text_input("Nombre de la empresa", "Mi empresa")
    periodo = st.date_input("Mes que se analiza", value=date.today().replace(day=1), format="DD/MM/YYYY")
    responsable = st.text_input("Responsable del informe", "")
    st.markdown("---")
    st.markdown("### Cómo usarla")
    st.caption("1. Ingresa los valores del mes cerrado.")
    st.caption("2. Separa costos directos de gastos operativos.")
    st.caption("3. Revisa indicadores, alertas y punto de equilibrio.")
    st.caption("4. Descarga el resumen para conservarlo.")
    st.markdown("---")
    st.caption("Los resultados dependen de la calidad de los datos ingresados. No reemplaza estados financieros certificados.")

st.markdown("### 1. Ingresos del mes")
st.caption("Registra ingresos causados del mes, sin duplicar IVA u otros impuestos recaudados para terceros.")
c1, c2, c3 = st.columns(3)
with c1:
    ingresos_servicios = st.number_input("Ingresos por servicios / mano de obra (COP)", min_value=0.0, value=0.0, step=500000.0)
with c2:
    ingresos_repuestos = st.number_input("Ingresos por repuestos y materiales (COP)", min_value=0.0, value=0.0, step=500000.0)
with c3:
    otros_ingresos = st.number_input("Otros ingresos operacionales (COP)", min_value=0.0, value=0.0, step=100000.0)

st.markdown("### 2. Costos directos del servicio")
st.caption("Costos directamente asociados a prestar el servicio o vender los repuestos. Evita contar dos veces un mismo concepto.")
a, b, c = st.columns(3)
with a:
    costo_repuestos = st.number_input("Costo de repuestos / materiales vendidos (COP)", min_value=0.0, value=0.0, step=250000.0)
with b:
    costo_tecnicos = st.number_input("Nómina y pagos directos de técnicos (COP)", min_value=0.0, value=0.0, step=250000.0)
with c:
    terceros = st.number_input("Servicios tercerizados / otros costos directos (COP)", min_value=0.0, value=0.0, step=100000.0)

st.markdown("### 3. Gastos operativos del mes")
with st.expander("Abrir gastos operativos", expanded=True):
    g1, g2, g3 = st.columns(3)
    with g1:
        nomina_admin = st.number_input("Nómina administrativa y comercial (COP)", min_value=0.0, value=0.0, step=250000.0)
        arriendo = st.number_input("Arriendo / administración del local (COP)", min_value=0.0, value=0.0, step=250000.0)
        servicios = st.number_input("Servicios públicos, internet y teléfono (COP)", min_value=0.0, value=0.0, step=100000.0)
    with g2:
        mercadeo = st.number_input("Mercadeo y publicidad (COP)", min_value=0.0, value=0.0, step=100000.0)
        transporte = st.number_input("Transporte, mensajería y logística (COP)", min_value=0.0, value=0.0, step=100000.0)
        mantenimiento = st.number_input("Mantenimiento, herramientas y equipos (COP)", min_value=0.0, value=0.0, step=100000.0)
    with g3:
        software = st.number_input("Software, honorarios y otros servicios (COP)", min_value=0.0, value=0.0, step=100000.0)
        depreciacion = st.number_input("Depreciación del mes (COP)", min_value=0.0, value=0.0, step=100000.0)
        otros_gastos = st.number_input("Otros gastos operativos (COP)", min_value=0.0, value=0.0, step=100000.0)

st.markdown("### 4. Gastos financieros e impuestos")
d1, d2, d3 = st.columns(3)
with d1:
    intereses = st.number_input("Intereses y gastos financieros (COP)", min_value=0.0, value=0.0, step=100000.0)
with d2:
    impuestos = st.number_input("Impuesto de renta / provisión del periodo (COP)", min_value=0.0, value=0.0, step=100000.0)
with d3:
    otros_no_operacionales = st.number_input("Otros gastos no operacionales (COP)", min_value=0.0, value=0.0, step=100000.0)

st.markdown("### 5. Caja, cartera y obligaciones")
st.caption("Estos datos complementan la utilidad: una empresa puede mostrar ganancias y aun así tener problemas de caja.")
f1, f2, f3 = st.columns(3)
with f1:
    caja = st.number_input("Saldo disponible en caja y bancos (COP)", min_value=0.0, value=0.0, step=250000.0)
    cartera = st.number_input("Cuentas por cobrar a clientes (COP)", min_value=0.0, value=0.0, step=250000.0)
with f2:
    inventario = st.number_input("Inventario actual (COP)", min_value=0.0, value=0.0, step=250000.0)
    pasivos_corrientes = st.number_input("Obligaciones por pagar en los próximos 12 meses (COP)", min_value=0.0, value=0.0, step=250000.0)
with f3:
    cuentas_proveedores = st.number_input("Deuda con proveedores incluida en obligaciones (COP)", min_value=0.0, value=0.0, step=250000.0)
    deuda_total = st.number_input("Deuda financiera total pendiente (COP)", min_value=0.0, value=0.0, step=250000.0)

st.markdown("### 6. Meta gerencial")
m1, m2 = st.columns(2)
with m1:
    utilidad_objetivo = st.number_input("Utilidad neta mensual deseada (COP)", min_value=0.0, value=0.0, step=500000.0)
with m2:
    margen_bruto_objetivo = st.slider("Margen bruto objetivo (%)", min_value=0, max_value=80, value=50, step=1)

# Calculations
ingresos = ingresos_servicios + ingresos_repuestos + otros_ingresos
costos_directos = costo_repuestos + costo_tecnicos + terceros
utilidad_bruta = ingresos - costos_directos
margen_bruto = (utilidad_bruta / ingresos * 100) if ingresos else 0.0
gastos_operativos = nomina_admin + arriendo + servicios + mercadeo + transporte + mantenimiento + software + depreciacion + otros_gastos
utilidad_operativa = utilidad_bruta - gastos_operativos
margen_operativo = (utilidad_operativa / ingresos * 100) if ingresos else 0.0
utilidad_antes_impuestos = utilidad_operativa - intereses - otros_no_operacionales
utilidad_neta = utilidad_antes_impuestos - impuestos
margen_neto = (utilidad_neta / ingresos * 100) if ingresos else 0.0
gastos_fijos_aprox = nomina_admin + arriendo + servicios + mercadeo + transporte + mantenimiento + software + depreciacion + otros_gastos + intereses + otros_no_operacionales
margen_contribucion = ((ingresos - costo_repuestos - terceros) / ingresos) if ingresos else 0.0
punto_equilibrio = (gastos_fijos_aprox / margen_contribucion) if margen_contribucion > 0 else None
venta_meta_utilidad = ((gastos_fijos_aprox + utilidad_objetivo) / margen_contribucion) if margen_contribucion > 0 else None
activos_corrientes = caja + cartera + inventario
razon_corriente = activos_corrientes / pasivos_corrientes if pasivos_corrientes > 0 else None
cobertura_caja = caja / pasivos_corrientes if pasivos_corrientes > 0 else None
rotacion_caja_dias = (caja / (costos_directos + gastos_operativos) * 30) if (costos_directos + gastos_operativos) > 0 else None

st.markdown("---")
st.markdown("## Resultado del diagnóstico")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Ingresos totales", money(ingresos))
k2.metric("Utilidad bruta", money(utilidad_bruta), pct(margen_bruto) + " margen bruto")
k3.metric("Utilidad operativa", money(utilidad_operativa), pct(margen_operativo) + " margen operativo")
k4.metric("Utilidad neta estimada", money(utilidad_neta), pct(margen_neto) + " margen neto")

if ingresos == 0:
    st.warning("Ingresa los ingresos del mes para calcular los márgenes y el punto de equilibrio.")
elif utilidad_neta < 0:
    st.error("Alerta: el resultado neto del mes es negativo. Revisa costos, gastos, precios y volumen de ventas.")
elif margen_bruto < margen_bruto_objetivo:
    st.warning(f"El margen bruto ({margen_bruto:.1f}%) está por debajo de tu objetivo ({margen_bruto_objetivo}%). Revisa precios, descuentos y costos directos.")
else:
    st.success("El margen bruto está en o por encima de la meta definida. Valida también caja, cartera y obligaciones.")

tabs = st.tabs(["📊 Indicadores", "⚖️ Punto de equilibrio", "💧 Liquidez y deuda", "🧭 Plan de acción", "📤 Exportar"])
with tabs[0]:
    st.markdown("#### Composición del resultado")
    chart_df = pd.DataFrame({
        "Concepto": ["Ingresos", "Costos directos", "Gastos operativos", "Gastos financieros y otros", "Impuestos", "Utilidad neta"],
        "Valor COP": [ingresos, costos_directos, gastos_operativos, intereses + otros_no_operacionales, impuestos, utilidad_neta]
    })
    fig = px.bar(chart_df, x="Concepto", y="Valor COP", title="Resultado mensual por concepto", text_auto=".2s")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", xaxis_title="", yaxis_title="COP")
    st.plotly_chart(fig, use_container_width=True)
    mix_df = pd.DataFrame({
        "Línea": ["Servicios / mano de obra", "Repuestos y materiales", "Otros ingresos"],
        "Ingresos COP": [ingresos_servicios, ingresos_repuestos, otros_ingresos]
    })
    fig2 = px.pie(mix_df, names="Línea", values="Ingresos COP", title="Composición de ingresos", hole=0.45)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("El costo de nómina de técnicos se incluye como costo directo en este modelo. Mantén un criterio contable consistente mes a mes.")

with tabs[1]:
    st.markdown("#### Punto de equilibrio estimado")
    if punto_equilibrio is None:
        st.info("No se puede calcular con los datos actuales: revisa que los ingresos sean mayores que los costos variables considerados.")
    else:
        pe1, pe2, pe3 = st.columns(3)
        pe1.metric("Ventas para punto de equilibrio", money(punto_equilibrio))
        pe2.metric("Ventas actuales", money(ingresos))
        pe3.metric("Diferencia frente al equilibrio", money(ingresos - punto_equilibrio))
        if ingresos >= punto_equilibrio:
            st.success("Con los supuestos ingresados, las ventas están por encima del punto de equilibrio.")
        else:
            st.error("Con los supuestos ingresados, las ventas no alcanzan el punto de equilibrio.")
        if venta_meta_utilidad is not None and utilidad_objetivo > 0:
            st.metric("Ventas estimadas para lograr la utilidad deseada", money(venta_meta_utilidad))
        st.caption("Estimación simplificada: trata los costos de repuestos y tercerizados como variables y los demás gastos como fijos. Ajusta esta clasificación a la realidad del negocio.")

with tabs[2]:
    st.markdown("#### Capacidad de pago de corto plazo")
    l1, l2, l3 = st.columns(3)
    l1.metric("Activos corrientes informados", money(activos_corrientes))
    l2.metric("Obligaciones corrientes", money(pasivos_corrientes))
    l3.metric("Caja disponible", money(caja))
    if razon_corriente is not None:
        st.metric("Razón corriente", f"{razon_corriente:.2f}x")
        if razon_corriente < 1:
            st.warning("Los activos corrientes informados son inferiores a las obligaciones de corto plazo.")
        elif razon_corriente < 1.5:
            st.info("Liquidez positiva, pero conviene vigilar recaudo de cartera y vencimientos.")
        else:
            st.success("La razón corriente es superior a 1,5x; revisa calidad de cartera e inventario para completar el análisis.")
    else:
        st.info("Ingresa las obligaciones corrientes para calcular la razón corriente.")
    if cobertura_caja is not None:
        st.metric("Cobertura inmediata con caja", f"{cobertura_caja:.2f}x")
    st.write("**Deuda financiera total pendiente:**", money(deuda_total))
    st.write("**Deuda con proveedores incluida en obligaciones:**", money(cuentas_proveedores))
    st.caption("La razón corriente es una señal inicial, no una conclusión por sí sola. El inventario puede tardar en convertirse en efectivo y la cartera puede tener riesgo de mora.")

with tabs[3]:
    st.markdown("#### Lectura gerencial automática")
    acciones = []
    if ingresos <= 0:
        acciones.append("Registra ingresos reales antes de interpretar los indicadores.")
    else:
        if margen_bruto < margen_bruto_objetivo:
            acciones.append(f"Revisar margen bruto: hoy es {margen_bruto:.1f}% frente al objetivo de {margen_bruto_objetivo}%. Analizar precios, descuentos, costo de repuestos y mezcla de servicios.")
        else:
            acciones.append("Mantener el control de costos directos y validar que el margen se sostenga en los siguientes meses.")
        if utilidad_operativa < 0:
            acciones.append("Reducir o redimensionar gastos operativos y revisar productividad/capacidad instalada; la operación no cubre los gastos actuales.")
        if utilidad_neta < 0:
            acciones.append("Preparar un plan de recuperación de rentabilidad y flujo de caja; priorizar gastos esenciales y renegociar compromisos cuando sea posible.")
        if punto_equilibrio is not None and ingresos < punto_equilibrio:
            acciones.append(f"Definir acciones comerciales para superar el punto de equilibrio estimado de {money(punto_equilibrio)} al mes.")
        if pasivos_corrientes > 0 and razon_corriente is not None and razon_corriente < 1:
            acciones.append("Construir un calendario semanal de pagos y recaudos; revisar cartera vencida, inventario lento y obligaciones próximas.")
        if margen_bruto >= margen_bruto_objetivo and utilidad_neta > 0:
            acciones.append("Evaluar mejoras de rentabilidad sin comprometer la calidad del servicio ni la liquidez.")
    for i, accion in enumerate(acciones, 1):
        st.markdown(f"**{i}.** {accion}")
    st.info("Esta lectura es orientativa y se basa únicamente en los valores ingresados; confirma los resultados con tu contador o estados financieros.")

with tabs[4]:
    st.markdown("#### Resumen descargable")
    fecha_txt = periodo.strftime("%Y-%m")
    datos = {
        "Empresa": empresa,
        "Periodo": fecha_txt,
        "Responsable": responsable,
        "Moneda": "COP",
        "Ingresos servicios": ingresos_servicios,
        "Ingresos repuestos": ingresos_repuestos,
        "Otros ingresos": otros_ingresos,
        "Ingresos totales": ingresos,
        "Costos directos": costos_directos,
        "Utilidad bruta": utilidad_bruta,
        "Margen bruto (%)": margen_bruto,
        "Gastos operativos": gastos_operativos,
        "Utilidad operativa": utilidad_operativa,
        "Margen operativo (%)": margen_operativo,
        "Intereses y gastos financieros": intereses,
        "Otros gastos no operacionales": otros_no_operacionales,
        "Impuestos": impuestos,
        "Utilidad neta": utilidad_neta,
        "Margen neto (%)": margen_neto,
        "Punto de equilibrio estimado": punto_equilibrio if punto_equilibrio is not None else "",
        "Ventas para utilidad objetivo": venta_meta_utilidad if venta_meta_utilidad is not None else "",
        "Caja y bancos": caja,
        "Cartera": cartera,
        "Inventario": inventario,
        "Obligaciones corrientes": pasivos_corrientes,
        "Deuda financiera total": deuda_total,
        "Activos corrientes informados": activos_corrientes,
        "Razón corriente": razon_corriente if razon_corriente is not None else "",
        "Margen bruto objetivo (%)": margen_bruto_objetivo,
    }
    resumen_df = pd.DataFrame([datos])
    st.dataframe(resumen_df, use_container_width=True)
    csv = resumen_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Descargar diagnóstico en CSV", data=csv, file_name=f"ROELSTAR_Diagnostico_{fecha_txt}.csv", mime="text/csv", use_container_width=True)
    st.caption("El archivo CSV se puede abrir en Excel. Los datos de esta sesión no se guardan automáticamente en un servidor.")

st.markdown("---")
st.markdown("<div class='small-note'>ROELSTAR · Herramienta gerencial de apoyo. Los indicadores dependen de la clasificación de costos y gastos, del periodo contable y de la calidad de los datos.</div>", unsafe_allow_html=True)
